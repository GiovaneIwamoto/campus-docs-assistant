import streamlit as st
from services.web_scraper import get_rendered_webpage
from services.pinecone_service import initialize_pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter

def run_indexing_mode(config: dict):
    """
    Run the indexing mode to scrape a web page and index its content into Pinecone.
    """
    web_url = config.get("web_url")
    pinecone_api_key = config.get("pinecone_api_key")
    pinecone_index_name = config.get("pinecone_index_name")
    embedding_model = config.get("embedding_model")

    try:
        with st.spinner("Processing the web page content...", show_time=True):

            # Initialize Pinecone
            vector_store = initialize_pinecone(pinecone_api_key, pinecone_index_name, embedding_model)

            # Load and chunk the web page content
            doc = get_rendered_webpage(web_url)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            all_splits = text_splitter.split_documents([doc])

            # Display the number of chunks
            st.status(f"Number of chunks created: {len(all_splits)}",state="complete")

            # Index the chunks
            vector_store.add_documents(documents=all_splits)

        st.success(f"Web page content indexed successfully at Pinecone!", icon=":material/cloud_done:")

    except Exception as e:
        st.error(f"An error occurred: {e}", icon=":material/error:")