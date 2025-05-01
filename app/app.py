import streamlit as st
from ui.layout import set_page_config, display_banner, initialize_chat_history, display_chat_history
from ui.sidebar import configure_sidebar
from services.chat_service import handle_user_input
from services.indexing_service import run_web_indexing_mode, run_file_indexing_mode

def main():
    # Set up the Streamlit page configuration
    set_page_config()
    
    # Retrieve API key and indexing mode configuration from the sidebar
    indexing_mode_config = configure_sidebar()

    # Initialize chat history in session state
    initialize_chat_history()

    # Display UI components
    display_banner()
    display_chat_history()

    # Handle web URL indexing mode
    if indexing_mode_config["web_indexing_enabled"]:
        run_web_indexing_mode(indexing_mode_config)

    # Handle file upload indexing mode
    if indexing_mode_config["file_indexing_enabled"]:
        uploaded_file = indexing_mode_config["uploaded_files"]
        run_file_indexing_mode(indexing_mode_config, uploaded_file)

    # Handle user input
    if prompt := st.chat_input():
        handle_user_input(prompt)

if __name__ == "__main__":
    main()