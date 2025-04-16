from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PineconeException

def initialize_vectorstore(api_key: str, index_name: str, embedding_model: str) -> PineconeVectorStore:
    """
    Initialize the vector store using Pinecone and Ollama embeddings.
    
    Args:
        api_key (str): Pinecone API key.
        index_name (str): Name of the Pinecone index.
        embedding_model (str): Model name for Ollama embeddings.
    
    Returns:
        PineconeVectorStore: Initialized vector store.
    
    Raises:
        ValueError: If any of the required parameters are missing.
        RuntimeError: If initialization of Pinecone or index fails.
    """
    # Validate parameters
    if not api_key:
        raise ValueError("Pinecone API key is required.")
    if not index_name:
        raise ValueError("Pinecone index name is required.")
    if not embedding_model:
        raise ValueError("Embedding model name is required.")

    # Initialize Pinecone client
    try:
        pinecone = Pinecone(api_key=api_key)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Pinecone client: {str(e)}") from e

    # Connect to existing index
    try:
        index = pinecone.Index(index_name)
    except PineconeException as e:
        raise RuntimeError(f"Failed to connect to Pinecone index '{index_name}'.") from e

    # Initialize embeddings
    try:
        embeddings = OllamaEmbeddings(model=embedding_model)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embeddings with model '{embedding_model}'.") from e

    # Initialize vector store
    try:
        vectorstore = PineconeVectorStore(embedding=embeddings, index=index)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize PineconeVectorStore: {str(e)}") from e

    return vectorstore
