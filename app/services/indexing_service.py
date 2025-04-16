import streamlit as st
from services.web_scraper import get_rendered_webpage
from services.vectorstore_service import initialize_vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter

def run_indexing_mode(config: dict):
    """
    Run the indexing mode to scrape a web page and index its content into Pinecone.
    
    Args:
        config (dict): Configuration dictionary containing the web URL, Pinecone API key,
                       Pinecone index name, and embedding model.
    """
    # Set configuration parameters
    web_url = config.get("web_url")
    pinecone_api_key = config.get("pinecone_api_key")
    pinecone_index_name = config.get("pinecone_index_name")
    embedding_model = config.get("embedding_model")

    try:
        with st.spinner("Processing web page and indexing...", show_time=True):

            # Initialize Pinecone
            vector_store = initialize_vectorstore(pinecone_api_key, pinecone_index_name, embedding_model)
            st.toast('Pinecone initialized successfully!', icon=":material/table_eye:")

            # Load and chunk the web page content
            doc = get_rendered_webpage(web_url)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            all_splits = text_splitter.split_documents([doc])
            st.toast('Web page content chunked successfully!', icon=":material/package:")

            # Display the number of chunks
            st.status(f"Number of chunks created: {len(all_splits)}",state="complete")

            # Index the chunks
            vector_store.add_documents(documents=all_splits)
            st.toast('Chunks indexed successfully!', icon=":material/cloud_upload:")

        st.success(f"Web page content indexed successfully at Pinecone!", icon=":material/cloud_done:")

    except ValueError as ve:
        st.error(f"Value error occurred: {ve}", icon=":material/cloud_off:")
        with st.expander("Error details"):
            st.exception(ve)

    except RuntimeError as re:
        st.error(f"Runtime error occurred: {re}", icon=":material/cloud_off:")
        with st.expander("Error details"):
            st.exception(re)

    except Exception as e:
        st.error(f"An unexpected error occurred during indexing process.", icon=":material/cloud_off:")
        with st.expander("Error details"):
            st.exception(e)