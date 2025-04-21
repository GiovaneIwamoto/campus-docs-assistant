import streamlit as st
from langchain_core.messages import HumanMessage

def set_page_config():
    # Set the page configuration for the Streamlit app
    st.set_page_config(
        page_title="Campus Docs Assistant",
        page_icon=":material/collections_bookmark:",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/GiovaneIwamoto/campus-docs-assistant/wiki',
            'Report a bug': "https://github.com/GiovaneIwamoto/campus-docs-assistant/issues",
            'About': ""
        }
    )

def display_banner():
    st.image("assets/banner.png")

def display_chat_history():
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message(name="user", avatar=":material/face:").write(msg.content)
        else:
            st.chat_message(name="assistant", avatar=":material/smart_toy:").write(msg.content)