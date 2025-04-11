import streamlit as st
from langchain.schema import ChatMessage
from langgraph.checkpoint.memory import MemorySaver

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            ChatMessage(role="assistant", content="How can I assist you with campus resources today?")
        ]
    if "memory" not in st.session_state:
        st.session_state["memory"] = MemorySaver()
