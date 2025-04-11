from ui.layout import display_banner, display_chat_history
from ui.sidebar import get_maritalk_api_key
from core.chat_session import initialize_chat_history
from services.maritalk_service import process_user_input
from config.logging_config import setup_logging
import streamlit as st

if __name__ == "__main__":
    setup_logging()

    api_key = get_maritalk_api_key()
    initialize_chat_history()
    display_banner()
    display_chat_history()

    if prompt := st.chat_input():
        process_user_input(prompt, api_key)

