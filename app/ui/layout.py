import streamlit as st
from langchain_core.messages import HumanMessage
from langchain.schema import ChatMessage

def set_page_config():
    # Set the page configuration for the Streamlit app
    st.set_page_config(
        page_title="Campus Docs Assistant",
        page_icon=":material/collections_bookmark:",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/GiovaneIwamoto/campus-docs-assistant',
            'Report a bug': "https://github.com/GiovaneIwamoto/campus-docs-assistant/issues",
            'About': """
            ### Thanks for checking out the project!
            If you find it useful, please consider giving it a ★ on [GitHub](https://github.com/GiovaneIwamoto/campus-docs-assistant).
            It really helps support the project and keeps it growing! Your feedback and support are greatly appreciated!"""
        }
    )

def display_banner():
    st.image("assets/banner.png")

def initialize_chat_history():
    """Initialize chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            ChatMessage(role="assistant", content="How can I assist you with campus resources today?")
        ]

def display_chat_history():
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message(name="user", avatar=":material/face:").write(msg.content)
        else:
            st.chat_message(name="assistant", avatar=":material/smart_toy:").write(msg.content)