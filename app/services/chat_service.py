import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.maritalk import MaritalkHTTPError
from core.chat_utils import format_chat_messages
from services.state_machine import app
from config.logging_config import setup_logging

logger = setup_logging()

def handle_user_input(prompt: str, api_key: str):
    """
    Handle user input by appending it to the chat history, invoking the LLM, 
    and updating the session state with the response.
    """
    if not api_key:
        st.info("Please add your LLM API key.", icon=":material/passkey:")
        return

    # Store the API key in session state
    st.session_state["api_key"] = api_key

    # Append the user's message to the chat history
    st.session_state["messages"].append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    try:
        # Invoke the state machine to process the input
        output = app.invoke(
            {"messages": st.session_state["messages"]},
            {"configurable": {"thread_id": "12345abcd"}}
        )

        # Update the session state with the new chat history
        st.session_state["messages"] = output["messages"]
        logger.info(f"Chat history:\n{format_chat_messages(output['messages'])}\n")

    except MaritalkHTTPError as e:
        logger.error(f"API Error: {e}")
        st.error("Invalid API key. Please enter a valid one.", icon=":material/key_off:")