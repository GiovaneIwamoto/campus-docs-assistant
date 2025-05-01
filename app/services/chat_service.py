import uuid
import streamlit as st
from config.logging_config import setup_logging, EnhancedLogger
from services.state_machine import app
from utils.error_handler import handle_maritalk_error, handle_runtime_error, handle_unexpected_error
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.maritalk import MaritalkHTTPError

logger = EnhancedLogger(setup_logging())

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
        st.toast("Please add your LLM API key.", icon=":material/passkey:")
        logger.warning("LLM API Key is missing. User cannot proceed without it.")
        return
    
    # Define the Pinecone API key
    pinecone_api_key = st.session_state.get("pinecone_api_key")
    if not pinecone_api_key:
        st.toast("Please add your Pinecone API key.", icon=":material/passkey:")
        logger.warning("LLM API Key is missing. User cannot proceed without it.")
        return

    # Define the Pinecone index name
    pinecone_index_name = st.session_state.get("pinecone_index_name")
    if not pinecone_index_name:
        st.toast("Please add your Pinecone index name.", icon=":material/passkey:")
        logger.warning("Pinecone index name is missing. User cannot proceed without it.")
        return

    # Loggers for auditing authentication
    logger.auth(llm_api_key, pinecone_api_key, pinecone_index_name)

    # Initialize the chat history if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Append the user's message to the chat history
    st.session_state["messages"].append(HumanMessage(content=prompt))
    st.chat_message("user", avatar=":material/face:").write(prompt)

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

        # Update the session state with the new chat history
        st.session_state["messages"] = output["messages"]
        logger.chat_history(output["messages"])

    except MaritalkHTTPError as e:
        logger.error("Maritalk API", e)
        handle_maritalk_error(e)

    except RuntimeError as re:
        logger.error("Runtime state machine invocation", re)
        handle_runtime_error(re)

    except Exception as e:
        logger.error("Unexpected state machine invocation", e)
        handle_unexpected_error(e)
