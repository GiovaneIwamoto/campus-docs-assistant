import logging
import streamlit as st
from langchain.schema import ChatMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.chat_models import ChatMaritalk
from langchain_community.chat_models.maritalk import MaritalkHTTPError
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from rich.logging import RichHandler

def format_chat_messages(messages: list) -> str:
    """
    Formats a list of chat message objects into a readable string representation.

    Args:
        messages (list): A list of message objects. Each object is expected to have 
                        the attributes `content` and `id`, and optionally `role`.

    Returns:
        str: A formatted string where each message is represented on a new line.
    """
    formatted = []
    for msg in messages:
        role = msg.role if hasattr(msg, "role") else msg.__class__.__name__
        formatted.append(f"[{role}] {msg.content} (ID: {msg.id})")
    return "\n".join(formatted)

# Configure Streamlit page settings
st.set_page_config(page_title="Capiara Algorithm Mentor", page_icon="", layout="wide")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",handlers=[RichHandler(rich_tracebacks=True, markup=True)])
logger = logging.getLogger(__name__)

# Display image banner
st.image("images/banner.png")

class StreamHandler(BaseCallbackHandler):
    """Handles real-time streaming of LLM-generated tokens in Streamlit."""
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Appends new tokens to the response and updates the UI dynamically."""
        self.text += token
        self.container.markdown(self.text)


def get_maritalk_api_key() -> str:
    """Retrieves the Maritalk API key from the sidebar input field."""
    with st.sidebar:
        return st.text_input("Maritalk API Key", type="default")


def initialize_chat_history() -> None:
    """Initializes chat history in session state if not already present."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]


def display_chat_history() -> None:
    """Displays the chat history stored in session state."""
    for msg in st.session_state["messages"]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.chat_message(role).write(msg.content)

# Define the chat prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that help students solving algorithms problems! Your name is CapIAra."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Initialize global memory for conversation persistence
if "memory" not in st.session_state:
    st.session_state["memory"] = MemorySaver()

def call_model(state: MessagesState) -> dict:
    """
    Calls the Maritalk model to generate a response based on the provided message state.

    This function interacts with the Maritalk API to generate a response using the specified
    language model. It ensures the API key is available, trims the input messages to fit
    within token limits, and streams the model's response back to the user.

    Args:
        state (MessagesState): A dictionary-like object containing the current state of messages.
            It should include a "messages" key with a list of message objects.

    Returns:
        dict: A dictionary containing the updated message history under the "messages" key.

    Raises:
        StopExecution: If the API key is not provided in the session state.
    """
    api_key = st.session_state.get("api_key")

    if not api_key:
        st.info("Please add your Maritalk API key to continue.", icon=":material/passkey:")
        st.stop()

    # Initialize the Maritalk chat model
    llm = ChatMaritalk(
        model="sabia-3",
        api_key=api_key,
        max_tokens=1000,
        stream=True,
        callbacks=[],
    )

    # Trim messages to fit within token limits
    trimmer = trim_messages(
        max_tokens=100,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )

    trimmed_messages = trimmer.invoke(state["messages"])
    logger.info(f"\nTrimmed messages:\n\n{format_chat_messages(trimmed_messages)}\n")

    prompt = prompt_template.invoke(
        {"messages": trimmed_messages}
    )
    logger.info(f"\nChat prompt:\n\n{prompt}\n")

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm.callbacks = [stream_handler]

        response = ""
        for chunk in llm.stream(prompt):
            response += chunk.content

        full_history = state["messages"] + [AIMessage(content=response)]
        return {"messages": full_history}

# Define workflow for processing user input
workflow = StateGraph(state_schema=MessagesState)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

app = workflow.compile(checkpointer=st.session_state["memory"])

def process_user_input(prompt: str, api_key: str) -> None:
    """
    Processes user input in a chatbot interface using the Maritalk API.

    This function handles user interactions by appending messages to the session state, 
    validating the API key, and invoking the chatbot API to generate responses. 

    Args:
        prompt (str): The user's input message.
        api_key (str): The API key required to authenticate with the Maritalk service.
    """
    
    # FIXME: Messages append is causing the chat history to be duplicated
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not api_key:
        st.info("Please add your Maritalk API key to continue.", icon=":material/passkey:")
        st.stop()

    try:
        # Store the API key in session state
        st.session_state["api_key"] = api_key

        input_messages = st.session_state["messages"] + [HumanMessage(prompt)]

        output = app.invoke(
            {"messages": input_messages},
            {"configurable": {"thread_id": "12345abcd"}},
        )

        # Update session state with the new chat history
        st.session_state["messages"] = output["messages"]
        logger.info(f"\nChat history:\n\n{format_chat_messages(output['messages'])}\n")

    except MaritalkHTTPError as e:
        logger.error(f"API Error: {e}")
        st.error("Invalid Maritalk API key, please enter a valid one.", icon=":material/key_off:")
        st.stop()


# Main application logic
if __name__ == "__main__":
    maritalk_api_key = get_maritalk_api_key()
    initialize_chat_history()
    display_chat_history()
    
    if prompt := st.chat_input():
        process_user_input(prompt, maritalk_api_key)
