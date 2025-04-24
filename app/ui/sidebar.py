import streamlit as st

def configure_sidebar() -> dict:
    """"Configure the sidebar for the Streamlit app."""

    with st.sidebar:
        # Settings for LLM API key and Pinecone configuration        
        keys_expander = st.expander("Settings", expanded=True)

        # Variables for LLM API key and Pinecone configuration
        llm_api_key = keys_expander.text_input("Maritalk API Key", type="password")
        pinecone_api_key = keys_expander.text_input("Pinecone API Key", type="password")
        pinecone_index_name = keys_expander.text_input("Pinecone Index Name")
        embedding_model = keys_expander.text_input("Ollama Embedding Model", value="nomic-embed-text")

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
        index_expander = st.expander("Indexing", expanded=True)

        # Web indexing section
        web_url = index_expander.text_input("Web Link", placeholder="https://example.com")
        web_indexing_enabled = index_expander.button("Activate Web Indexing", icon=":material/database_upload:")

        # File indexing section
        uploaded_files = index_expander.file_uploader("File Upload", type=["pdf", "txt", "docx", "zip"], accept_multiple_files=True)
        file_indexing_enabled = index_expander.button("Activate File Indexing", icon=":material/database_upload:")

    # Validate required fields for web indexing
    if web_indexing_enabled:
        if not web_url or not pinecone_api_key or not pinecone_index_name or not embedding_model:
            st.toast(
                "Web Indexing failed — you must provide a valid URL and fill in all the required fields.",
                icon=":material/assignment_late:"
            )
            web_indexing_enabled = False
        else:
            st.toast("Web indexing activated!",icon=":material/check_circle:")

    # Validate required fields for file indexing
    if file_indexing_enabled:
        if not uploaded_files or not pinecone_api_key or not pinecone_index_name or not embedding_model:
            st.toast(
                "File indexing failed — please upload a file and fill in all the required fields.",
                icon=":material/assignment_late:"
            )
            file_indexing_enabled = False
        else:
            st.toast(f"File indexing activated!", icon=":material/check_circle:")

    indexing_mode_config = {
        "web_indexing_enabled": web_indexing_enabled,
        "web_url": web_url,
        "file_indexing_enabled": file_indexing_enabled,   
        "uploaded_files": uploaded_files,                   
        "pinecone_api_key": pinecone_api_key,
        "pinecone_index_name": pinecone_index_name,
        "embedding_model": embedding_model,
    }

    return indexing_mode_config