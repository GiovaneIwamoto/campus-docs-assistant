import streamlit as st
from config.logging_config import setup_logging
from utils.chat_utils import format_chat_messages
from core.handlers import StreamHandler
from template.prompts import chat_prompt_template
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, MessagesState
from langchain_community.chat_models import ChatMaritalk
from langchain_community.chat_models.maritalk import MaritalkHTTPError
from langchain_core.messages import AIMessage, trim_messages

logger = setup_logging()

def call_model(state: MessagesState) -> dict:
    """
    Call the Maritalk model to generate a response based on the provided message state.
    """
    api_key = st.session_state.get("api_key")
    if not api_key:
        st.info("Please add your API key.")
        st.stop()

    # Initialize the Maritalk chat model
    llm = ChatMaritalk(
        model="sabia-3",
        api_key=api_key,
        max_tokens=1000,
        stream=True,
        callbacks=[],
    )

    # Trim messages to fit within token limits
    trimmer = trim_messages(
        max_tokens=1000,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )
    trimmed_messages = trimmer.invoke(state["messages"])
    logger.info(f"Trimmed messages:\n{format_chat_messages(trimmed_messages)}\n")

    # Generate the prompt
    prompt = chat_prompt_template.invoke({"messages": trimmed_messages})
    logger.info(f"Prompt:\n{prompt}\n")

    # Stream the response
    with st.chat_message("assistant"):
        try:
            handler = StreamHandler(st.empty())
            llm.callbacks = [handler]
            
            response = ""
            for chunk in llm.stream(prompt):
                response += chunk.content
            
            return {"messages": state["messages"] + [AIMessage(content=response)]}
        
        except MaritalkHTTPError as e:
            st.write("Ops, something went wrong.")
            raise e

# Define the state machine workflow
workflow = StateGraph(state_schema=MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# Initialize memory for conversation persistence
if "memory" not in st.session_state:
    st.session_state["memory"] = MemorySaver()

app = workflow.compile(checkpointer=st.session_state["memory"])