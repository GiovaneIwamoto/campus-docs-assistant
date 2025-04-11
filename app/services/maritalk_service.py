import streamlit as st
from config.logging_config import setup_logging
from core.chat_utils import format_chat_messages
from services.state_machine import app
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.maritalk import MaritalkHTTPError

logger = setup_logging()

def process_user_input(prompt: str, api_key: str):
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    if not api_key:
        st.info("Please add your Maritalk API key.", icon=":material/passkey:")
        st.stop()

    st.session_state["api_key"] = api_key
    input_messages = st.session_state["messages"] + [HumanMessage(content=prompt)]

    try:
        output = app.invoke(
            {"messages": input_messages},
            {"configurable": {"thread_id": "12345abcd"}}
        )
        st.session_state["messages"] = output["messages"]
        logger.info(f"\nChat history:\n{format_chat_messages(output['messages'])}")

    except MaritalkHTTPError as e:
        logger.error(f"API Error: {e}")
        st.error("Invalid API key", icon=":material/key_off:")
        st.stop()
