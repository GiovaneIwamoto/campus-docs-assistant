import streamlit as st
from langchain_core.messages import HumanMessage

def display_banner():
    st.image("assets/banner.png")

def display_chat_history():
    for msg in st.session_state["messages"]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.chat_message(role).write(msg.content)
