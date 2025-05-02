import streamlit as st
from typing_extensions import TypedDict, List
from config.logging_config import setup_logging, EnhancedLogger
from core.handlers import StreamHandler
from services.vectorstore_service import initialize_vectorstore
from template.rag_prompt import RAG_SYSTEM_PROMPT
from template.tool_decision_prompt import TOOL_DECISION_SYSTEM_PROMPT
from utils.tool_call_parser import parse_tool_call
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from langchain_core.tools import tool
from langchain_community.chat_models import ChatMaritalk
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

logger = EnhancedLogger(setup_logging())

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

    return ChatMaritalk(
        model="sabia-3",
        api_key=llm_api_key,
        max_tokens=50000,
        temperature=0.2,
        stream=stream,
        callbacks=[],
    )

@tool(response_format="content_and_artifact")
def retrieve(query: str, pinecone_api_key: str, pinecone_index_name: str, embedding_model: str) -> tuple[str, List]:
    """Retrieve relevant documents based on the user query about university files and related subjects."""
    try:
        logger.tool_query("Retrieve with query", query)

        # Initialize the vector store
        vector_store = initialize_vectorstore(
            api_key=pinecone_api_key,
            index_name=pinecone_index_name,
            embedding_model=embedding_model
        )  

        # Perform the similarity search     
        retrieved_docs = vector_store.similarity_search(query, k=3)
        logger.tool_document("Documents found", retrieved_docs)

        # Serialize the retrieved documents
        serialized = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}"
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    except RuntimeError as re:
        error_msg = f"Tool Error {str(re)}"
        logger.error("Runtime error in 'retrieve' tool", re)
        return error_msg, []
    
    except Exception as e:
        error_msg = f"Tool Error {str(e)}"
        logger.error("Unexpected error in 'retrieve' tool", e)
        return error_msg, []

def query_or_respond(state: MessagesState):
    """Handles the logic for querying or responding based on the user's input and system instructions."""
    llm_api_key = st.session_state.get("llm_api_key")

    # Initialize the LLM without streaming for tool detection
    # At this point, there is no need to stream for tool detection
    llm_for_tools = initialize_llm(llm_api_key, stream=False) 

    # Create a copy of messages for trimming excluding system message
    history_for_trimming = [msg for msg in state["messages"] if msg.type != "system"]
    
    logger.initializing()

    # Trim messages to fit within the token limit from the LLM
    trimmer = trim_messages(
        max_tokens=40000,
        strategy="last",
        token_counter=llm_for_tools,
        include_system=False,
        allow_partial=False,
        start_on="human",
    )

    trimmed_messages = trimmer.invoke(history_for_trimming)

    # Log trimmed messages for debugging
    logger.trimmer("All state messages excluding system", trimmed_messages)

    # Generate system instructions that is oriented to generate the tool call or not
    tool_decision_system_prompt = TOOL_DECISION_SYSTEM_PROMPT.format(
        pinecone_api_key=st.session_state.get("pinecone_api_key"),
        pinecone_index_name=st.session_state.get("pinecone_index_name"),
        embedding_model=st.session_state.get("embedding_model")
    )

    prompt = [SystemMessage(content=tool_decision_system_prompt)] + trimmed_messages
    
    # Call the LLM to get initial response
    logger.llm_decision("Validating", "Checking if tool call is needed")
    
    response = llm_for_tools.invoke(prompt)
    content = response.content.strip()
    
    logger.llm_response("Response content", content)
    
    # Check if it looks like a JSON response starts with open brace
    if content.startswith('{'):
        st.toast("I will use the tool to get more information, please wait a moment.", icon=":material/robot:")
        logger.llm_decision("Analyzing", "Potential tool call detected")
        
        # Try to balance braces if they're unbalanced
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces > close_braces:
            logger.llm_decision("Detected unbalanced braces", f"{open_braces} opening vs {close_braces} closing")
            # Add missing closing braces
            content = content + ('}' * (open_braces - close_braces))
            response.content = content

        # Check if the response contains a tool call
        tool_call = parse_tool_call(response)
    
        if tool_call:
            # At AI message add the tool call attribute so it can be processed later
            response.tool_calls = [tool_call]    
            
            # Add response to history for tool processing
            state["messages"].append(response)
            return {"messages": [response]}
    
    # No tool call detected
    else:
        logger.llm_decision("No tool call detected", "Generating and streaming final response")
        # For direct answers use streaming in UI
        with st.chat_message("assistant", avatar=":material/mindfulness:"):
            stream_container = st.empty()
            stream_handler = StreamHandler(stream_container)
            
            # Initialize streaming LLM for direct response
            streaming_llm = initialize_llm(llm_api_key, stream=True)
            streaming_llm.callbacks = [stream_handler]
            
            # Generate a new streaming response
            accumulated_response = ""
            for chunk in streaming_llm.stream(prompt):
                if chunk.content:
                    accumulated_response += chunk.content
            
            # Create final message and add to history
            ai_message = AIMessage(content=accumulated_response)
            state["messages"].append(ai_message)
            return {"messages": state["messages"]}
        
def generate(state: MessagesState):
    """Generate the final response using the tool's content."""
    llm_api_key = st.session_state.get("llm_api_key")

    logger.llm_with_tools("Generating final response using knowledge base")

    # Get recent tool messages to extract context
    recent_tool_messages = [
        m for m in reversed(state["messages"]) if m.type == "tool"
    ][::-1]
    
    logger.llm_tool_response("Recent tool messages", recent_tool_messages)
    
    # Check if any tool messages were found
    if not recent_tool_messages:
        logger.error("ToolMessage not found", "Cannot generate final response.")
        raise RuntimeError("Error obtaining tool response.")

    # Check if the last tool message contains an error
    last_tool_msg = recent_tool_messages[0]
    if "Tool Error" in last_tool_msg.content:
        last_tool_msg.content = last_tool_msg.content.replace("Tool Error", "")

        # Remove last AI message from history to avoid message displaying in UI
        if st.session_state["messages"] and isinstance(st.session_state["messages"][-1], AIMessage):
            st.session_state["messages"].pop()

        raise RuntimeError(last_tool_msg.content)

    # Extract context from tool responses
    docs_content = "\n\n".join(t.content for t in recent_tool_messages)

    # Filter conversation messages to include only human messages
    conversation_messages = [
        m for m in st.session_state["messages"] if isinstance(m, HumanMessage)
    ]
    logger.llm_tool_response("All human conversation messages", conversation_messages)

    # Get the last human message
    if conversation_messages:
        last_human_message = conversation_messages[-1]
        logger.llm_tool_last_message("Last human message", last_human_message.content)
    else:
        logger.warning("No human messages found in the conversation history.")

    # Generate the system prompt for RAG
    rag_system_prompt = RAG_SYSTEM_PROMPT.format(context=docs_content)

    # Create the final prompt for the LLM last human message and context
    prompt = [SystemMessage(content=rag_system_prompt), HumanMessage(content=last_human_message.content)] 

    # Stream the response to UI
    with st.chat_message("assistant", avatar=":material/psychology:"):
        stream_container = st.empty()
        stream_handler = StreamHandler(stream_container)
        
        # Re-initialize LLM with streaming for UI
        streaming_llm = initialize_llm(llm_api_key, stream=True)
        streaming_llm.callbacks = [stream_handler]
        
        # Stream response chunks to UI
        accumulated_response = ""
        for chunk in streaming_llm.stream(prompt):
            if chunk.content:
                accumulated_response += chunk.content
        
        # Remove last AI message from history to avoid tool call messsage persisting to next query
        if st.session_state["messages"] and isinstance(st.session_state["messages"][-1], AIMessage):
            st.session_state["messages"].pop()

        # Create final message and add to history
        ai_message = AIMessage(content=accumulated_response)
        st.session_state["messages"].append(ai_message)
        return {"messages": st.session_state["messages"]}


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