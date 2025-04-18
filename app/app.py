import streamlit as st
from ui.layout import set_page_config, display_banner, display_chat_history
from ui.sidebar import configure_sidebar
from core.state_manager import initialize_chat_history
from services.chat_service import handle_user_input
from services.indexing_service import run_indexing_mode
from config.logging_config import setup_logging

logger = setup_logging()

def main():
    # Configure logging
    setup_logging()

    # Set up the Streamlit page configuration
    set_page_config()
    
    # Retrieve API key and indexing mode configuration from the sidebar
    indexing_mode_config = configure_sidebar()

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
        handle_user_input(prompt)

if __name__ == "__main__":
    main()