import time
import streamlit as st
from config.logging_config import setup_logging

logger = setup_logging()

def handle_maritalk_error(error: Exception):
    """
    Handle errors related to the Maritalk API, specifically invalid API keys.
    This function logs the error and provides feedback to the user.
    
    Args:
        error (Exception): The exception raised by the Maritalk API.
    """
    st.toast("Invalid Maritalk API key. Please check your credentials.", icon=":material/passkey:")        

    # Clear chat history and reset session state
    with st.chat_message("system", avatar=":material/psychology_alt:"):    
        with st.spinner("Restarting chat history"):
            time.sleep(6)
            st.session_state.clear()
            st.rerun()

def handle_runtime_error(error: Exception):
    """
    Handle runtime errors that occur during the execution of the application.
    This function logs the error and provides feedback to the user.
    
    Args:
        error (Exception): The exception raised during runtime.
    """
    st.toast(f"An error occurred: {error}", icon=":material/database_off:")
    
    # Clear chat history and reset session state
    with st.chat_message("system", avatar=":material/psychology_alt:"):    
        with st.spinner("Restarting chat history"):
            time.sleep(6)
            st.session_state.clear()
            st.rerun()

def handle_unexpected_error(error: Exception):
    """
    Handle unexpected errors that occur during the execution of the application.
    This function logs the error and provides feedback to the user.
    
    Args:
        error (Exception): The exception raised during runtime.
    """
    st.toast("An unexpected error occurred. Please try again later.", icon=":material/sync_problem:")    
    
    # Clear chat history and reset session state
    with st.chat_message("system", avatar=":material/psychology_alt:"):    
        with st.spinner("Restarting chat history"):
            time.sleep(6)
            st.session_state.clear()
            st.rerun()