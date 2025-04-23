![image_banner](image/banner.png)

![image_rag_flow](image/rag_flow.png)

![image_install_guide](image/install_guide.png)

### **INTRODUCTION**

The **Campus Docs Assistant** is a powerful AI-driven application designed to assist students and faculty members of the Federal University of Mato Grosso do Sul (UFMS) in accessing legal, academic, and administrative documents. This tool simplifies the process of retrieving information about university policies, mandatory internships, enrollment procedures, faculty contacts, and more. By leveraging state-of-the-art AI technologies, the assistant provides accurate, concise, and context-aware responses to user queries.

The project integrates cutting-edge tools such as **LangChain**, **Pinecone**, **Ollama**, and **Streamlit** to deliver a seamless and interactive user experience. It is built with modularity, scalability, and maintainability in mind, making it a robust solution for academic and administrative needs.

---

### **AVATARS**

| Avatar                            | Usage                                   | Meaning |
|-----------------------------------|-----------------------------------------|-------------------------------------------|
| ![face](/assets/face.svg)                     | User messages                           | Represents the user interacting with the assistant.                   |
| ![smart_toy](/assets/smart_toy.svg)           | Assistant messages                      | Represents the AI assistant responses to the user.                    |
| ![mindfulness](/assets/mindfulness.svg)       | Assistant streaming direct responses    | Represents responses generated using the model's own knowledge.       |
| ![psychology](/assets/psychology.svg)         | Assistant streaming tool-based responses| Represents intelligence and analysis during tool-based responses.     |
| ![cognition](/assets/cognition.svg)           | Assistant during indexing operations    | Represents cognitive processing during indexing tasks.                |
| ![psychology_alt](/assets/psychology_alt.svg) | System messages during errors           | Represents system-level guidance or chat history resets.              |

This legend provides a clear understanding of the avatars used in the application and their significance in different contexts.

---

### **FEATURES**

**AI-Powered Query Handling**

- **Maritalk Integration**: The assistant uses the Maritalk Large Language Model to process user queries and generate intelligent responses. Maritalk is optimized for conversational AI and supports advanced natural language understanding.
- **Tool Decision System**: The assistant evaluates user queries to decide whether to call external tool or respond directly based on the conversation context.

**Document Retrieval with Pinecone**

- **Vector Search**: The assistant uses Pinecone, a high-performance vector database, to perform similarity searches. This allows it to retrieve the most relevant documents based on the user's query.
- **Ollama Embeddings**: The assistant leverages Ollama's embedding models to convert text into vector representations, enabling efficient and accurate similarity searches.

**Context-Aware Responses**

- **Retrieve and Generate**: The assistant combines retrieved document content with user queries to generate precise and context-aware responses. This is achieved using LangChain's RAG capabilities.
- **Dynamic Context Management**: The assistant maintains a clean and concise conversation history, ensuring that responses are relevant and free from unnecessary information.

**Web Scraping and Indexing**

- **Playwright Integration**: The assistant uses Playwright to scrape and render web pages, enabling it to index external content into Pinecone for future queries.
- **Chunking with LangChain**: The assistant splits large documents into manageable chunks using LangChain's text splitters, ensuring efficient indexing and retrieval.

**Interactive User Interface**

- **Streamlit Framework**: The assistant features an intuitive and interactive UI built with Streamlit. Users can input queries, view responses, and configure settings directly from the web interface.
- **Real-Time Feedback**: The assistant provides real-time feedback through toasts, spinners, and dynamic updates, enhancing the user experience.

**Modular and Scalable Architecture**

- **LangChain State Machine**: The assistant uses LangChain's state machine and ToolNode to manage the flow of interactions, ensuring modularity and scalability.
- **Error Handling**: Comprehensive error handling mechanisms are in place to manage runtime errors, API issues, and unexpected failures gracefully.

---

### **TECHNOLOGIES**

**LangChain**

- **Prompt Engineering**: Custom prompts for tool decision-making and RAG.
- **State Management**: Managing conversation history and tool calls.
- **Text Processing**: Splitting and formatting text for efficient retrieval and response generation.

**LangGraph**

- **Conversational Flow Control**: Defining dynamic workflows using nodes and edges to handle tool calls, decision-making, and state transitions.
- **State Management**: Persisting and transitioning structured conversation states across different stages like query interpretation, tool usage, and response generation.
- **Tool Integration**: Seamlessly incorporating LangChain tools and LLMs in a modular and traceable way, enabling complex interactions with memory, branching, and fallback handling.

**Pinecone**

- **Similarity Search**: Retrieving the most relevant documents based on user queries.
- **Scalability**: Handling large datasets with low latency and high throughput.

**Ollama**

- **Text Vectorization**: Converting text into vector representations for similarity search.
- **Custom Embeddings**: Supporting domain-specific embeddings for academic and administrative content.

**Maritalk**

- **Natural Language Understanding**: Processing user queries and generating intelligent responses.
- **Conversational AI**: Supporting dynamic and context-aware interactions.

**Streamlit**

- **Web Interface**: Building an interactive and user-friendly UI.
- **Real-Time Updates**: Providing dynamic feedback and updates to users.

**Playwright**

- **Web Scraping**: Rendering and extracting content from web pages.
- **Automation**: Automating the process of indexing external content.

---

### **INSTALLATION GUIDE**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/GiovaneIwamoto/campus-docs-assistant.git
   cd campus-docs-assistant
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright**
   ```bash
   pip install playwright
   playwright install
   ```

5. **Run the Application**
   ```bash
   cd app
   streamlit run app.py
   ```

---

### **USAGE**

### **1. Query Handling**
- Enter your query in the chat input box.
- The assistant will decide whether to call a tool or respond directly.

### **2. Document Retrieval**
- Queries related to university documents will trigger the retrieve tool.
- The assistant will fetch the most relevant documents from Pinecone and generate a response.

### **3. Web Scraping and Indexing**
- Use the sidebar to enable indexing mode.
- Enter a URL to scrape and index its content into Pinecone.

### **4. Configuration**
- Use the sidebar to configure API keys, Pinecone index name, and embedding model.
