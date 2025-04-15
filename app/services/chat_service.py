import uuid
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.maritalk import MaritalkHTTPError
from utils.chat_utils import format_chat_messages
from utils.error_handler import handle_maritalk_error
from config.logging_config import setup_logging
from services.state_machine import app

logger = setup_logging()

def handle_user_input(prompt: str, llm_api_key: str):
    """
    Handle user input by appending it to the chat history, invoking the LLM, 
    and updating the session state with the response.
    """
    if not llm_api_key:
        st.info("Please add your LLM API key.", icon=":material/passkey:")
        return

    # Store the API key in session state
    st.session_state["api_key"] = llm_api_key

    # Initialize the chat history if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Append the user's message to the chat history
    st.session_state["messages"].append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    try:
        # Invoke the state machine to process the input
        thread_id = str(uuid.uuid4())
        output = app.invoke(
            {"messages": st.session_state["messages"]},
            {"configurable": {"thread_id": thread_id}}
        )

        # Update the session state with the new chat history
        st.session_state["messages"] = output["messages"]
        logger.info(f"[#FFA500][CHAT HISTORY][/#FFA500] [#4169E1][All session state messages][/#4169E1]\n\n{format_chat_messages(output['messages'])}\n\n\n")

    except MaritalkHTTPError as e:
        handle_maritalk_error(e)