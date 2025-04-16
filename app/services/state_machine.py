import re
import json
import uuid
import streamlit as st
from typing_extensions import TypedDict, List
from config.logging_config import setup_logging
from core.handlers import StreamHandler
from services.vectorstore_service import initialize_vectorstore
from utils.chat_utils import format_chat_messages
from langchain_core.messages import AIMessage, SystemMessage, trim_messages
from langchain_core.tools import tool
from langchain_community.chat_models import ChatMaritalk
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

logger = setup_logging()

# Define the state for the graph
class MessagesState(TypedDict):
    messages: List

def initialize_llm(llm_api_key: str, stream: bool = True) -> ChatMaritalk:
    """
    Initialize the Maritalk chat model with the provided API key.
    
    Args:
        llm_api_key (str): The API key for the Maritalk model.
        stream (bool): Whether to enable streaming.
    
    Returns:
        ChatMaritalk: An instance of the Maritalk chat model.
    """
    # OpenAI tools schema it is not relevant to binding tools to the LLM
    tools_schema = [
        {
            "type": "function",
            "function": {
                "name": "retrieve",
                "description": "Retrieve relevant documents from the knowledge base given a user query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's question or query to search in the vector database."
                        },
                        "pinecone_api_key": {
                            "type": "string",
                            "description": "Pinecone API key for authentication."
                        },
                        "pinecone_index_name": {
                            "type": "string",
                            "description": "Name of the Pinecone index to search."
                        },
                        "embedding_model": {
                            "type": "string",
                            "description": "The embedding model to use for vectorization."
                        }
                    },
                    "required": ["query", "pinecone_api_key", "pinecone_index_name", "embedding_model"],
                    "additionalProperties": False
                }
            }
        }
    ]

    return ChatMaritalk(
        model="sabia-3",
        api_key=llm_api_key,
        max_tokens=100000,
        temperature=0.2,
        stream=stream,
        callbacks=[],
        tools=tools_schema,
    )

@tool(response_format="content_and_artifact")
def retrieve(query: str, pinecone_api_key: str, pinecone_index_name: str, embedding_model: str) -> tuple[str, List]:
    """Retrieve relevant documents based on the user query about university files and related subjects."""

    if not pinecone_api_key or not pinecone_index_name or not embedding_model:
        error_message = "Pinecone API key, Index Name and Embedding Model are required."
        logger.error(f"Error in 'retrieve' tool: {error_message}")
        return error_message, []

    try:
        logger.info(f"[#26F5C9][TOOL][/#26F5C9] [#4169E1][Retrieve with query][/#4169E1] {query}\n")

        # Initialize the vector store
        vector_store = initialize_vectorstore(
            api_key=pinecone_api_key,
            index_name=pinecone_index_name,
            embedding_model=embedding_model
        )  

        # Perform the similarity search     
        retrieved_docs = vector_store.similarity_search(query, k=3)
        logger.info(f"\n[#26F5C9][TOOL][/#26F5C9] [#4169E1][Documents found][/#4169E1] -> {len(retrieved_docs)}\n")

        # Serialize the retrieved documents
        serialized = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}"
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs
    
    except ValueError as ve:
        # Handle missing parameters
        logger.error(f"Validation error in 'retrieve' tool: {ve}")
        return f"Validation Error: {ve}", []

    except RuntimeError as re:
        # Handle runtime errors Pinecone or embeddings initialization issues
        logger.error(f"Runtime error in 'retrieve' tool: {re}")
        return f"Runtime Error: {re}", []

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in 'retrieve' tool: {e}")
        return "An unexpected error occurred while retrieving documents.", []

def parse_tool_call(response):
    """
    Parse the tool call from the LLM response.   
    
    Args:
        response: The response object from the LLM.
    
    Returns:
        dict: Parsed tool call with function name and arguments or None if parsing fails.
    """
    try:
        # Get the raw content from the response and normalize it
        content = response.content.strip()
        normalized_content = re.sub(r"\s+", " ", content)

        # Attempt to parse the content as JSON directly
        try:
            parsed = json.loads(normalized_content)
        
        # Try extracting JSON using regex
        except json.JSONDecodeError:
            logger.info("[#FF4F4F][PARSER][/#FF4F4F] Attempting regex extraction\n")

            json_pattern = r'(\{.*\})'
            match = re.search(json_pattern, normalized_content)
            if match:
                try:
                    parsed = json.loads(match.group(1))
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse JSON even with regex.\n")
                    return None
            else:
                logger.info("[#FF4F4F][PARSER][/#FF4F4F] No JSON pattern found\n")
                return None

        # Validate the parsed JSON structure
        if "tool_call" in parsed:
            call = parsed["tool_call"]

            # Ensure required fields are present
            if "function" not in call or "arguments" not in call:
                logger.error(f"Invalid tool call format.\n")
                return None

            # Map the tool call to the expected format
            call["name"] = call.pop("function", "")
            call["args"] = call.pop("arguments", {})
            call["id"] = call.get("id", str(uuid.uuid4()))
            return call
        else:
            logger.warning("No 'tool_call' field found in the parsed JSON.")
            return None
        
    except Exception as e:
        logger.error(f"Error parsing tool call: {e}")
        return None

def generate_system_instructions():
    """Generate the system instructions dynamically with Pinecone parameters from session state."""
    # Retrieve Pinecone parameters from session state
    pinecone_api_key = st.session_state.get("pinecone_api_key")
    pinecone_index_name = st.session_state.get("pinecone_index_name")
    embedding_model = st.session_state.get("embedding_model")

    # Generate dynamic system instructions
    system_instructions = f"""
    You are a helpful assistant with access to a specialized document database containing information related to university files and related subjects.
    ONLY call the tool 'retrieve' (by returning a JSON object as specified below) if the user's query is clearly about this domain.
    If the user's query is about general topics or subjects not related to this domain, answer directly without calling any tool. 

    When calling the tool, respond ONLY with a JSON object in the following format and NOTHING else:
    {{
        "tool_call": {{
            "function": "retrieve",
            "arguments": {{
                "query": "<your query>",
                "pinecone_api_key": "{pinecone_api_key}",
                "pinecone_index_name": "{pinecone_index_name}",
                "embedding_model": "{embedding_model}"
            }}
        }}
    }}

    If no external specialized information is required, answer directly.
    """
    return system_instructions

def query_or_respond(state: MessagesState):
    """Handles the logic for querying or responding based on the user's input and system instructions."""
    llm_api_key = st.session_state.get("llm_api_key")

    # Initialize the LLM without streaming for tool detection
    # At this point, there is no need to stream for tool detection
    llm_for_tools = initialize_llm(llm_api_key, stream=False) 

    # Create a copy of messages for trimming excluding system message
    history_for_trimming = [msg for msg in state["messages"] if msg.type != "system"]
    
    logger.info("[#18F54A][INITIALIZING][/#18F54A]\n")

    # Trim only the conversation history without the system message
    # This is to ensure we don't exceed the context window limit for the LLM
    trimmer = trim_messages(
        max_tokens=1000, # Fix this later
        strategy="last",
        token_counter=llm_for_tools,
        include_system=False,
        allow_partial=False,
        start_on="human",
    )

    trimmed_messages = trimmer.invoke(history_for_trimming)

    # Log trimmed messages for debugging
    logger.info(f"[#FFA500][TRIMMED MESSAGES][/#FFA500] [#4169E1][All state messages excluding system][/#4169E1]\n\n{format_chat_messages(trimmed_messages)}\n")

    # Generate system instructions that is oriented to generate the tool call or not
    system_instructions = generate_system_instructions()

    # Create the prompt with system with trimmed conversation
    prompt = [SystemMessage(content=system_instructions)] + trimmed_messages

    # Log prompt for debugging
    logger.info(f"[#FFA500][PROMPT QUERY OR RESPOND][/#FFA500] [#4169E1][System message with trimmed][/#4169E1]\n\n{format_chat_messages(prompt)}\n")
    
    # Log status for tool detection
    logger.info("[#6819B3][LLM][/#6819B3] [#4169E1][Validating][/#4169E1] Checking if tool call is needed\n")
    
    # Call the LLM to check if a tool call is needed
    response = llm_for_tools.invoke(prompt)

    # Log the response for debugging
    logger.info(f"[#6819B3][LLM][/#6819B3] [#4169E1][Response][/#4169E1]{response.content}\n")
    
    # Check if the response contains a tool call
    tool_call = parse_tool_call(response)
    
    # Tool call detected
    if tool_call:
        # At AI message add the tool call attribute so it can be processed later
        response.tool_calls = [tool_call]
        # Add response to history for tool processing
        state["messages"].append(response)
        return {"messages": [response]}
    
    # No tool call detected
    else:
        logger.info("[#6819B3][LLM][/#6819B3] [#4169E1][No tool call detected][/#4169E1] Generating direct response\n")
        # For direct answers, use streaming in UI
        with st.chat_message("assistant"):
            stream_container = st.empty()
            stream_handler = StreamHandler(stream_container)
            
            # Initialize streaming LLM for direct response
            streaming_llm = initialize_llm(llm_api_key, stream=True)
            streaming_llm.callbacks = [stream_handler]
            
            # Generate a new, streaming response
            accumulated_response = ""
            for chunk in streaming_llm.stream(prompt):
                if chunk.content:
                    accumulated_response += chunk.content
            
            # Create final message and add to history
            ai_message = AIMessage(content=accumulated_response)
            state = {"messages": st.session_state["messages"]}
            st.session_state["messages"].append(ai_message)
        
def generate(state: MessagesState):
    """Generate the final response using the tool's content."""
    llm_api_key = st.session_state.get("llm_api_key")

    # Initialize LLM without streaming initially
    llm = initialize_llm(llm_api_key, stream=False)

    logger.info("[#6819B3][LLM TOOL][/#6819B3] [#4169E1]Generating final response using knowledge base[/#4169E1]\n")

    recent_tool_messages = [
        m for m in reversed(state["messages"]) if m.type == "tool"
    ][::-1]

    if not recent_tool_messages:
        logger.error("[ERROR] ToolMessage not found. Cannot generate final response.")
        return {"messages": state["messages"]}

    # Extract context from tool responses but don't add to history
    docs_content = "\n\n".join(t.content for t in recent_tool_messages)
    rag_system_message = (
        "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise.\n\n"
        f"Context:\n{docs_content}"
    )

    # Filter to get only conversation messages (no tools, no system)
    conversation_messages = [
        m for m in state["messages"]
        if m.type in ("human", "ai") and not getattr(m, "tool_calls", [])
    ]
    
    # Trim the conversation if needed
    trimmer = trim_messages(
        max_tokens=1000,
        strategy="last",
        token_counter=llm,
        include_system=False,
        allow_partial=False,
        start_on="human",
    )
    
    trimmed_conversation = trimmer.invoke(conversation_messages)
    
    # Compose final prompt with system first, then conversation
    prompt = [SystemMessage(content=rag_system_message)] + trimmed_conversation

    # Stream the response to UI
    with st.chat_message("assistant"):
        stream_container = st.empty()
        stream_handler = StreamHandler(stream_container)
        
        # Re-initialize LLM with streaming for UI
        streaming_llm = initialize_llm(llm_api_key, stream=True)  # Pass stream=True
        streaming_llm.callbacks = [stream_handler]
        
        # Stream response chunks to UI
        accumulated_response = ""
        for chunk in streaming_llm.stream(prompt):
            if chunk.content:
                accumulated_response += chunk.content
        
        # Create final message and add to history
        ai_message = AIMessage(content=accumulated_response)
        result = {"messages": [ai_message]}
        st.session_state["messages"].extend(result["messages"])


# Build the state graph
builder = StateGraph(MessagesState)
builder.add_node("query_or_respond", query_or_respond)
tool_node = ToolNode([retrieve])
builder.add_node("tools", tool_node)
builder.add_node("generate", generate)

# Define entry point
builder.set_entry_point("query_or_respond")

# Define conditional edges
builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {"tools": "tools", END: END},
)
builder.add_edge("tools", "generate")
builder.add_edge("generate", END)

# Compile the graph
graph = builder.compile()

# Initialize memory for conversation persistence
if "memory" not in st.session_state:
    st.session_state["memory"] = MemorySaver()

app = graph.with_config(checkpointer=st.session_state["memory"])