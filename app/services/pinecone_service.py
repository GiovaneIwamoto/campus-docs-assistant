from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

def initialize_pinecone(api_key: str, index_name: str, embedding_model: str):
    """
    Initialize Pinecone and return the vector store.
    """
    pinecone = Pinecone(api_key=api_key)
    index = pinecone.Index(index_name)
    
    embeddings = OllamaEmbeddings(model=embedding_model)
    vector_store = PineconeVectorStore(embedding=embeddings, index=index)
    
    return vector_store