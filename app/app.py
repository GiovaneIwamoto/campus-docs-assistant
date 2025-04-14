import streamlit as st
from ui.layout import display_banner, display_chat_history
from ui.sidebar import configure_sidebar
from core.chat_session import initialize_chat_history
from services.chat_service import handle_user_input
from services.indexing_service import run_indexing_mode
from config.logging_config import setup_logging

logger = setup_logging()

def main():
    # Configure logging
    setup_logging()

    # Retrieve API key and indexing mode configuration from the sidebar
    llm_api_key, indexing_mode_config = configure_sidebar()

    # Initialize chat history in session state
    initialize_chat_history()

    # Display UI components
    display_banner()
    display_chat_history()

    # Handle indexing mode
    if indexing_mode_config["enabled"]:
        run_indexing_mode(indexing_mode_config)

    # Handle user input
    if prompt := st.chat_input():
        handle_user_input(prompt, llm_api_key)

if __name__ == "__main__":
    main()