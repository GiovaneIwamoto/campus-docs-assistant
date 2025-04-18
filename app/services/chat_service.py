import uuid
import streamlit as st
from config.logging_config import setup_logging
from services.state_machine import app
from utils.chat_utils import format_chat_messages
from utils.error_handler import handle_maritalk_error
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.maritalk import MaritalkHTTPError

logger = setup_logging()

def handle_user_input(prompt: str):
    """
    Handle user input by appending it to the chat history, invoking the LLM, 
    and updating the session state with the response.

    Args:
        prompt (str): The user's input message.        
    """
    # Check for LLM API key
    llm_api_key = st.session_state.get("llm_api_key")
    if not llm_api_key:
        st.info("Please add your LLM API key.", icon=":material/passkey:")
        logger.warning("LLM API Key is missing. User cannot proceed without it.\n")
        return
    
    # Define the Pinecone API key
    pinecone_api_key = st.session_state.get("pinecone_api_key")
    if not pinecone_api_key:
        st.info("Please add your Pinecone API key.", icon=":material/passkey:")
        logger.warning("LLM API Key is missing. User cannot proceed without it.\n")
        return

    # Define the Pinecone index name
    pinecone_index_name = st.session_state.get("pinecone_index_name")
    if not pinecone_index_name:
        st.info("Please add your Pinecone index name.", icon=":material/passkey:")
        logger.warning("Pinecone index name is missing. User cannot proceed without it.\n")
        return

    # Loggers for auditing authentication
    logger.info("\n[#2D0856][AUTH][/#2D0856] LLM API Key: %s", llm_api_key)
    logger.info("[#2D0856][AUTH][/#2D0856] Pinecone API Key: %s", pinecone_api_key)
    logger.info("[#2D0856][AUTH][/#2D0856] Pinecone Index Name: %s\n", pinecone_index_name)

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
            {
                "messages": st.session_state["messages"],
                "llm_api_key": llm_api_key,
                "pinecone_api_key": pinecone_api_key,
                "pinecone_index_name": pinecone_index_name,
            },
            {"configurable": {"thread_id": thread_id}}
        )

        # Check for errors in the output from state machine
        if isinstance(output, tuple) and len(output) == 2 and "Error" in output[0]:
            error_message = output[0]
            logger.error(f"Error returned by state machine: {error_message}\n")
            st.warning(error_message, icon=":material/sync_problem:")
            return

        # Update the session state with the new chat history
        st.session_state["messages"] = output["messages"]
        logger.info(f"[#FFA500][CHAT HISTORY][/#FFA500] [#4169E1][All session state messages][/#4169E1]\n\n{format_chat_messages(output['messages'])}\n\n\n")

    except ValueError as ve:
        logger.error(f"ValueError during state machine invocation: {ve}\n")
        st.error("An error occurred: {ve}", icon=":material/sync_problem:")

    except MaritalkHTTPError as e:
        logger.error(f"Maritalk API Error: {e}\n")
        handle_maritalk_error(e)

    except Exception as e:
        logger.error(f"Unexpected error during state machine invocation: {e}\n")
        st.error("An unexpected error occurred. Please try again later.", icon=":material/sync_problem:")