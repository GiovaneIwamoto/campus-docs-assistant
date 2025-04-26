import os
import streamlit as st
from langchain_core.documents import Document
from services.vectorstore_service import initialize_vectorstore
from utils.text_extractor import extract_text_from_file
from utils.file_extractor import extract_files_from_zip, FileExtractorError
from utils.web_scraper import get_rendered_webpage
from langchain_text_splitters import RecursiveCharacterTextSplitter

def run_web_indexing_mode(config: dict):
    """
    Run the web indexing mode to scrape a web page and index its content into Pinecone.
    
    Args:
        config (dict): Configuration dictionary containing the web URL, Pinecone API key,
                       Pinecone index name, and embedding model.
    """
    # Set configuration parameters
    web_url = config.get("web_url")
    pinecone_api_key = config.get("pinecone_api_key")
    pinecone_index_name = config.get("pinecone_index_name")
    embedding_model = config.get("embedding_model")

    with st.chat_message("assistant", avatar=":material/cognition_2:"):
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

                st.status(f"Web page content indexed successfully at Pinecone!", state="complete")

        except ValueError as ve:
            st.toast(f"A value error occurred during indexing process.", icon=":material/settings_alert:")
            with st.expander("Error details"):
                st.write(f"A value error occurred: {ve}")

        except RuntimeError as re:
            st.toast(f"A runtime error occurred during indexing process.", icon=":material/database_off:")
            with st.expander("Error details"):
                st.write(f"A runtime error occurred: {re}")

        except Exception as e:
            st.toast(f"An unexpected error occurred during indexing process.", icon=":material/cloud_off:")
            with st.expander("Error details"):
                st.write(f"An unexpected error occurred: {e}")

def run_file_indexing_mode(config: dict, uploaded_files: list):
    """
    Run the file indexing mode to extract text from uploaded files and index the content into Pinecone.

    Args:
        config (dict): Configuration dictionary containing Pinecone credentials and embedding model.
        file: The uploaded file from Streamlit's file_uploader.
    """
    # Set configuration parameters
    pinecone_api_key = config.get("pinecone_api_key")
    pinecone_index_name = config.get("pinecone_index_name")
    embedding_model = config.get("embedding_model")
    
    with st.chat_message("assistant", avatar=":material/cognition_2:"):
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[-1].lower()
            
            # If the uploaded file is a ZIP archive extract its contents
            if file_extension == ".zip":
                try:
                    with st.spinner(f"Extracting files from ZIP: {file.name}"):
                        extracted_items = extract_files_from_zip(file)
                    
                    # Warn the user if no supported files were found in the ZIP    
                    if not extracted_items:
                        st.toast(f"No supported files found in {file.name}", icon=":material/folder_zip:")
                        with st.expander("Error details"):
                            st.write(f"An error occurred: {e}")
                        continue
                    
                    # Process each extracted file individually                                
                    for inner_filename, inner_file in extracted_items:
                        inner_ext = os.path.splitext(inner_filename)[-1].lower()
                        try:
                            process_file_for_indexing(inner_file, inner_filename, inner_ext, pinecone_api_key, pinecone_index_name, embedding_model)
                        except Exception as e:
                            st.toast(f"Error processing file '{inner_filename}': {e}", icon=":material/folder_zip:")
                            with st.expander("Error details"):
                                st.write(f"An error occurred: {e}")

                except FileExtractorError as e:
                    st.toast(f"Error extracting ZIP file '{file.name}': {e}", icon=":material/folder_zip:")
                    with st.expander("Error details"):
                        st.write(f"An error occurred: {e}")
                    continue
            
            # Regular simple file process it directly    
            else:
                try:
                    process_file_for_indexing(
                        file, file.name, file_extension,
                        pinecone_api_key, pinecone_index_name, embedding_model
                    )
                except Exception as e:
                    st.toast(f"Error processing file '{file.name}': {e}", icon=":material/feedback:")
                    with st.expander("Error details"):
                        st.write(f"An error occurred: {e}")

def process_file_for_indexing(file_obj, filename, file_ext, pinecone_api_key, pinecone_index_name, embedding_model):
    """
    Process a single file for indexing into Pinecone.

    Args:
        file_obj: The uploaded file object.
        filename (str): The name of the file.
        file_ext (str): The file extension.
        pinecone_api_key (str): Pinecone API key.
        pinecone_index_name (str): Pinecone index name.
        embedding_model (str): Embedding model to use.
    """
    try:
        with st.spinner(f"Processing file {filename}..."):
            
            # Extract text from the uploaded file
            extracted_text = extract_text_from_file(file_obj, file_ext)
            st.toast('File content extracted successfully!', icon=":material/draft:")
            
            # Create a LangChain document
            doc = Document(page_content=extracted_text, metadata={"source": filename})
            st.toast('Pinecone initialized successfully!', icon=":material/table_eye:")
            
            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            all_splits = text_splitter.split_documents([doc])
            st.toast('File content chunked successfully!', icon=":material/package:")
            
            # Display number of chunks created
            st.status(f"Number of chunks created: {len(all_splits)}", state="complete")

            # Initialize Pinecone and index the chunks
            vector_store = initialize_vectorstore(pinecone_api_key, pinecone_index_name, embedding_model)
            vector_store.add_documents(documents=all_splits)
            st.toast('Chunks indexed successfully!', icon=":material/cloud_upload:")
            st.status(f"File {filename} indexed successfully at Pinecone!", state="complete")

    except ValueError as ve:
        st.toast(f"A value error occurred during indexing process.", icon=":material/settings_alert:")
        with st.expander("Error details"):
            st.write(f"A value error occurred: {ve}")

    except RuntimeError as re:
        st.toast(f"A runtime error occurred during indexing process.", icon=":material/database_off:")
        with st.expander("Error details"):
            st.write(f"A runtime error occurred: {re}")

    except Exception as e:
        st.toast(f"An unexpected error occurred during indexing process.", icon=":material/cloud_off:")
        with st.expander("Error details"):
            st.write(f"An unexpected error occurred: {e}")    