import streamlit as st

def configure_sidebar():
    """"Configure the sidebar for the Streamlit app."""

    with st.sidebar:
        st.title("Settings")
        
        # API key llm input
        llm_api_key = st.text_input("LLM API Key", type="password")

        # API key pinecone input
        pinecone_api_key = st.text_input("Pinecone API Key", type="password")
        
        # Pinecone index name input
        pinecone_index_name = st.text_input("Pinecone Index Name")
        
        # Embedding model input
        embedding_model = st.text_input("Embedding Model", value="nomic-embed-text")

        # Index mode configuration
        st.title("Indexing")

        web_url = st.text_input("Enter the URL to scrape:")
        
        # Button to activate indexing mode
        indexing_mode_enabled = st.button("Activate Indexing", icon=":material/database_upload:")

    # Validate required fields
    if indexing_mode_enabled:
        if not web_url or not pinecone_api_key or not pinecone_index_name or not embedding_model:
            st.warning(
                "**Indexing failed** — you must provide a valid URL and fill in all the required fields.",
                icon=":material/assignment_late:"
            )
            indexing_mode_enabled = False
        else:
            st.success("Indexing activated!",icon=":material/check_circle:")

    indexing_mode_config = {
        "enabled": indexing_mode_enabled,
        "web_url": web_url,
        "pinecone_api_key": pinecone_api_key,
        "pinecone_index_name": pinecone_index_name,
        "embedding_model": embedding_model,
    }

    return llm_api_key, indexing_mode_config