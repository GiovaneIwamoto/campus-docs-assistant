import streamlit as st

def configure_sidebar() -> dict:
    """"Configure the sidebar for the Streamlit app."""

    with st.sidebar:
        # Settings for LLM API key and Pinecone configuration
        st.title("Settings")
        
        # Variables for LLM API key and Pinecone configuration
        llm_api_key = st.text_input("Maritalk API Key", type="password")
        pinecone_api_key = st.text_input("Pinecone API Key", type="password")
        pinecone_index_name = st.text_input("Pinecone Index Name")
        embedding_model = st.text_input("Ollama Embedding Model", value="nomic-embed-text")

        # Initialization of session state variables
        if 'llm_api_key' not in st.session_state:
            st.session_state['llm_api_key'] = llm_api_key

        if 'pinecone_api_key' not in st.session_state:
            st.session_state['pinecone_api_key'] = pinecone_api_key  

        if 'pinecone_index_name' not in st.session_state:
            st.session_state['pinecone_index_name'] = pinecone_index_name
        
        if 'embedding_model' not in st.session_state:
            st.session_state['embedding_model'] = embedding_model

        # Update session state variables   
        st.session_state['llm_api_key'] = llm_api_key
        st.session_state['pinecone_api_key'] = pinecone_api_key  
        st.session_state['pinecone_index_name'] = pinecone_index_name
        st.session_state['embedding_model'] = embedding_model

        # Settings for indexing mode
        st.title("Indexing")

        # Web URL input and button for activating indexing
        web_url = st.text_input("Enter the URL to scrape:")
        indexing_mode_enabled = st.button("Activate Indexing", icon=":material/database_upload:")
        
        # File indexing section
        st.markdown("---")
        st.subheader("File Upload for Indexing")
        uploaded_file = st.file_uploader("Upload a file (.pdf, .txt, .docx):", type=["pdf", "txt", "docx"])
        file_indexing_enabled = st.button("Activate File Indexing", icon=":material/database_upload:")

    # Validate required fields for web indexing
    if indexing_mode_enabled:
        if not web_url or not pinecone_api_key or not pinecone_index_name or not embedding_model:
            st.toast(
                "Indexing failed — you must provide a valid URL and fill in all the required fields.",
                icon=":material/assignment_late:"
            )
            indexing_mode_enabled = False
        else:
            st.toast("Indexing activated!",icon=":material/check_circle:")

    if file_indexing_enabled:
        if not uploaded_file or not pinecone_api_key or not pinecone_index_name or not embedding_model:
            st.toast(
                "File indexing failed — please upload a file and fill in all the required fields.",
                icon=":material/assignment_late:"
            )
            file_indexing_enabled = False
        else:
            st.toast(f"File indexing activated for {uploaded_file.name}", icon=":material/check_circle:")

    indexing_mode_config = {
        "enabled": indexing_mode_enabled,
        "web_url": web_url,
        "file_indexing_enabled": file_indexing_enabled,   
        "uploaded_file": uploaded_file,                   
        "pinecone_api_key": pinecone_api_key,
        "pinecone_index_name": pinecone_index_name,
        "embedding_model": embedding_model,
    }

    return indexing_mode_config