import streamlit as st
from typing_extensions import TypedDict, List
from config.logging_config import setup_logging
from core.handlers import StreamHandler
from services.vectorstore_service import initialize_vectorstore
from template.rag_prompt import RAG_SYSTEM_PROMPT
from template.tool_decision_prompt import TOOL_DECISION_SYSTEM_PROMPT
from utils.chat_formatter import format_chat_messages
from utils.tool_call_parser import parse_tool_call
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
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

    except RuntimeError as re:
        error_msg = f"Tool Error {str(re)}"
        logger.error(f"Runtime error in 'retrieve' tool: {re}\n")
        return error_msg, []
    
    except Exception as e:
        error_msg = f"Tool Error {str(e)}"
        logger.error(f"Unexpected error in 'retrieve' tool: {e}\n")
        return error_msg, []

def query_or_respond(state: MessagesState):
    """Handles the logic for querying or responding based on the user's input and system instructions."""
    llm_api_key = st.session_state.get("llm_api_key")

    # Initialize the LLM without streaming for tool detection
    # At this point, there is no need to stream for tool detection
    llm_for_tools = initialize_llm(llm_api_key, stream=False) 

    # Create a copy of messages for trimming excluding system message
    history_for_trimming = [msg for msg in state["messages"] if msg.type != "system"]
    
    logger.info("[#18F54A][INITIALIZING][/#18F54A]\n")

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
    logger.info(f"[#FFA500][TRIMMED MESSAGES][/#FFA500] [#4169E1][All state messages excluding system][/#4169E1]\n\n{format_chat_messages(trimmed_messages)}\n")

    # Generate system instructions that is oriented to generate the tool call or not
    tool_decision_system_prompt = TOOL_DECISION_SYSTEM_PROMPT.format(
        pinecone_api_key=st.session_state.get("pinecone_api_key"),
        pinecone_index_name=st.session_state.get("pinecone_index_name"),
        embedding_model=st.session_state.get("embedding_model")
    )

    prompt = [SystemMessage(content=tool_decision_system_prompt)] + trimmed_messages
    
    # Call the LLM to get initial response
    logger.info("[#6819B3][LLM][/#6819B3] [#4169E1][Validating][/#4169E1] Checking if tool call is needed\n")
    
    response = llm_for_tools.invoke(prompt)
    content = response.content.strip()
    
    logger.info(f"[#6819B3][LLM][/#6819B3] [#4169E1][Response content][/#4169E1]\n{content}\n")
    
    # Check if it looks like a JSON response starts with open brace
    if content.startswith('{'):
        st.toast("I will use the tool to get more information, please wait a moment.", icon=":material/robot:")
        logger.info("[#6819B3][LLM][/#6819B3] [#4169E1][Potential tool call detected][/#4169E1]\n")
        
        # Try to balance braces if they're unbalanced
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces > close_braces:
            logger.info(f"[#6819B3][LLM][/#6819B3] [#4169E1][Detected unbalanced braces][/#4169E1] {open_braces} opening vs {close_braces} closing\n")
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
        logger.info("[#6819B3][LLM][/#6819B3] [#4169E1][No tool call detected][/#4169E1] Streaming generated response\n")
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

    logger.info("[#6819B3][LLM TOOL][/#6819B3] [#4169E1][Generating final response using knowledge base][/#4169E1]\n")

    # Get recent tool messages to extract context
    recent_tool_messages = [
        m for m in reversed(state["messages"]) if m.type == "tool"
    ][::-1]
    
    logger.info(f"[#6819B3][LLM TOOL][/#6819B3] [#4169E1][Recent tool messages][/#4169E1]\n\n{format_chat_messages(recent_tool_messages)}\n")
    
    # Check if any tool messages were found
    if not recent_tool_messages:
        logger.error("ToolMessage not found. Cannot generate final response.\n")
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
    logger.info(f"[#6819B3][LLM TOOL][/#6819B3] [#4169E1][Human last conversation messages][/#4169E1]\n\n{format_chat_messages(conversation_messages)}\n")

    # Get the last human message
    if conversation_messages:
        last_human_message = conversation_messages[-1]
        logger.info(f"[#6819B3][LLM TOOL][/#6819B3] [#4169E1][Last human message][/#4169E1] {last_human_message.content}\n")
    else:
        logger.warning("[#6819B3][LLM TOOL][/#6819B3] No human messages found in the conversation history\n")

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