import time
import streamlit as st
from config.logging_config import setup_logging

logger = setup_logging()

def handle_maritalk_error(error: Exception):
    """
    Handle errors related to the Maritalk API, specifically invalid API keys.
    This function logs the error and provides feedback to the user.
    It also clears the chat history and resets the session state.
    
    Args:
        error (Exception): The exception raised by the Maritalk API.
    """
    logger.error(f"API Error: {error}")

    st.error("Invalid API key please enter a valid one.", icon=":material/key_off:")

    # Clear chat history and reset session state
    with st.spinner("Restarting chat history"):
        time.sleep(4)
        st.session_state.clear()
        st.rerun()