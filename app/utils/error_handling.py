import time
import streamlit as st
from config.logging_config import setup_logging
from ui.layout import display_chat_history
from langchain_core.messages import ChatMessage

logger = setup_logging()

def handle_maritalk_error(error: Exception):
    """
    Handle MaritalkHTTPError by logging the error, displaying a message to the user,
    and resetting the session state.
    """
    logger.error(f"API Error: {error}")

    st.error("Invalid API key. Please enter a valid one.", icon=":material/key_off:")

    # Clear chat history and reset session state
    with st.spinner("Restarting chat history"):
        time.sleep(4)
        st.session_state.clear()
        st.rerun()