import streamlit as st
from ui.layout import display_banner, display_chat_history
from ui.sidebar import get_maritalk_api_key
from core.chat_session import initialize_chat_history
from services.chat_service import handle_user_input
from config.logging_config import setup_logging

def main():
    setup_logging()

    # Retrieve API key from the sidebar
    api_key = get_maritalk_api_key()

    # Initialize chat history in session state
    initialize_chat_history()

    # Display UI components
    display_banner()
    display_chat_history()

    # Handle user input
    if prompt := st.chat_input():
        handle_user_input(prompt, api_key)

if __name__ == "__main__":
    main()