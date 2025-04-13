import streamlit as st
from langchain.schema import ChatMessage

def initialize_chat_history():
    """Initialize chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            ChatMessage(role="assistant", content="How can I assist you with campus resources today?")
        ]