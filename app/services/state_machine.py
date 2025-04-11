import streamlit as st
from config.logging_config import setup_logging
from core.chat_utils import format_chat_messages
from core.handlers import StreamHandler
from template.prompts import chat_prompt_template

from langgraph.graph import StateGraph, START, MessagesState
from langchain_community.chat_models import ChatMaritalk
from langchain_core.messages import AIMessage, trim_messages

logger = setup_logging()

def call_model(state: MessagesState) -> dict:
    api_key = st.session_state.get("api_key")
    if not api_key:
        st.info("Please add your API key.")
        st.stop()

    llm = ChatMaritalk(
        model="sabia-3",
        api_key=api_key,
        max_tokens=1000,
        stream=True,
        callbacks=[],
    )

    trimmer = trim_messages(
        max_tokens=1000,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )

    trimmed_messages = trimmer.invoke(state["messages"])
    logger.info(f"Trimmed:\n{format_chat_messages(trimmed_messages)}")

    prompt = chat_prompt_template.invoke({"messages": trimmed_messages})
    logger.info(f"Prompt:\n{prompt}")

    with st.chat_message("assistant"):
        handler = StreamHandler(st.empty())
        llm.callbacks = [handler]

        response = ""
        for chunk in llm.stream(prompt):
            response += chunk.content

        return {"messages": state["messages"] + [AIMessage(content=response)]}

workflow = StateGraph(state_schema=MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")


if "memory" not in st.session_state:
    st.session_state["memory"] = None
    app = workflow.compile(checkpointer=st.session_state["memory"])
