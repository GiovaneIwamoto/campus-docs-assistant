import streamlit as st

def get_maritalk_api_key():
    with st.sidebar:
        return st.text_input("Maritalk API Key", type="default")
