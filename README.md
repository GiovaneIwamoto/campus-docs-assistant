![image_banner](image/banner.png)

![image_rag_flow](image/rag_flow.png)

![image_install_guide](image/install_guide.png)

### **INTRODUCTION**

The Campus Docs Assistant is an AI-powered platform designed to streamline access to academic and administrative information within universities. Through a user-friendly chatbot interface, students, faculty, and staff can interact naturally with an intelligent assistant capable of answering questions, retrieving official documents, and offering support grounded in institutional data. This natural language interaction simplifies complex information retrieval tasks, eliminating the need to manually navigate dense and often confusing documentation.

By leveraging state-of-the-art AI technologies, the assistant understands complex queries, performs context-aware document retrieval, and generates accurate and concise responses in real time. Its web-based interface ensures accessibility while promoting autonomy in accessing institutional knowledge. This makes the Campus Docs Assistant a valuable tool for educational institutions aiming to enhance user experience, reduce repetitive inquiries, and improve the overall efficiency of information management.

---

### **AVATARS**

| Avatar                         | Usage                       | Meaning                   |
|--------------------------------|-----------------------------|---------------------------|
| ![face](/assets/face.svg)                     | User messages                           | Represents the user interacting with the assistant              |
| ![smart_toy](/assets/smart_toy.svg)           | Assistant messages                      | Represents the AI assistant responses to the user               |
| ![mindfulness](/assets/mindfulness.svg)       | Assistant streaming direct responses    | Represents responses generated using the model's own knowledge  |
| ![psychology](/assets/psychology.svg)         | Assistant streaming tool-based responses| Represents intelligence and analysis during tool-based responses|
| ![cognition](/assets/cognition.svg)           | Assistant during indexing operations    | Represents cognitive processing during indexing tasks           |
| ![psychology_alt](/assets/psychology_alt.svg) | Assistant messages during errors        | Represents system-level guidance or chat history resets         |

This legend provides a clear understanding of the avatars used in the application and their significance in different contexts.

---

### **MOTIVATION**

This project was initially inspired by the specific challenges observed at the Federal University of Mato Grosso do Sul (UFMS), but the problem it addresses is common across many universities. In academic settings, students often struggle to obtain simple pieces of information due to the overwhelming complexity and volume of official documentation. Regulations, guidelines, and institutional policies are typically stored in dense, legalistic documents that are not user-friendly or easy to navigate.

In practice, students seeking a single answer — such as internship requirements, enrollment rules, or calendar dates — frequently end up reading through dozens of pages of official publications. Frustrated by this experience, many resort to contacting academic coordinators directly. However, from the administration's perspective, this creates a high volume of repetitive inquiries that could have been answered if students had easier access to the right part of the documentation.

This cycle results in inefficiency and dissatisfaction on both sides: students receive vague or delayed responses, and coordinators are overwhelmed by simple questions that require them to redirect students to existing official documents. The Campus Docs Assistant was developed to break this cycle, acting as a bridge between formal documentation and practical student needs. By enabling natural language interaction and intelligent information retrieval, it aims to reduce friction, save time, and promote autonomous access to institutional knowledge.

---

### **FEATURES**

**AI-Powered Query Handling**

- The assistant processes user queries using the Maritalk large language model, which is optimized for conversational AI and advanced natural language understanding.

- It includes a tool decision system that evaluates the context of each query to determine whether to generate a direct response or trigger external tools, ensuring intelligent and context-aware interactions.

**Smart Document Retrieval**

- The assistant performs semantic search using Pinecone, a high-performance vector database, allowing retrieval of the most relevant documents based on meaning rather than keywords.

- It uses Ollama embeddings to convert documents and user queries into vector representations, enabling fast and accurate similarity matching for academic and administrative content.

**Context-Aware Responses**

- Implements a retrieve and generate mechanism that blends user queries with retrieved content to produce accurate, relevant answers. Leveraging LangChain's Retrieval-Augmented Generation logic under the hood.

- Maintains dynamic context management, keeping the conversation history clean and focused to ensure that responses remain concise and contextually accurate.

**Web Scraping and Indexing**

- Integrates Playwright to render and scrape dynamic web pages, allowing the assistant to index and respond with external institutional content.

- Utilizes intelligent document chunking to split large texts into digestible parts for efficient indexing and retrieval, enabling high performance even with large datasets.

**Interactive User Interface**

- Built with Streamlit, the assistant features a responsive and interactive UI where users can submit queries, view answers, and configure behavior—all within an accessible web interface.

**Modular and Scalable Architecture**

- Employs a LangGraph-based state machine, where conversational logic is handled through dynamic workflows—ensuring flexibility in managing tool calls, memory, and state transitions.

- Designed with robust error handling to gracefully manage runtime issues, API failures, and unexpected user input across various system components.

---

### **INSTALLATION GUIDE**

**Clone the Repository**
```ruby
$ git clone https://github.com/GiovaneIwamoto/campus-docs-assistant.git
$ cd campus-docs-assistant
```

**Install Dependencies**
```ruby
$ pip install -r requirements.txt
```

**Install Playwright**
```ruby
$ pip install playwright
$ playwright install
```

**Run the Application**
```ruby
$ cd app
$ streamlit run app.py
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

---