from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

def initialize_vectorstore(api_key: str, index_name: str, embedding_model: str) -> PineconeVectorStore:
    """
    Initialize the vector store using Pinecone and Ollama embeddings.
    Args:
        api_key (str): Pinecone API key.
        index_name (str): Name of the Pinecone index.
        embedding_model (str): Model name for Ollama embeddings.
    Returns:
        PineconeVectorStore: Initialized vector store.
    """
    pinecone = Pinecone(api_key=api_key)
    index = pinecone.Index(index_name)
    
    embeddings = OllamaEmbeddings(model=embedding_model)
    vector_store = PineconeVectorStore(embedding=embeddings, index=index)
    
    return vector_store