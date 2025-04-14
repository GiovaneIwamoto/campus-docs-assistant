![banner](https://github.com/user-attachments/assets/7b4565af-c0b4-4bfb-bdaf-9859347b7677)

### **INTRODUCTION**

This project aims to facilitate access for students of the Federal University of Mato Grosso do Sul (UFMS) to legal and academic documents, such as requirements for mandatory internships, enrollment policies, among others.

[![Icons](https://skillicons.dev/icons?i=aws,py,theme=dark)](https://skillicons.dev)

---

### **INSTALLATION GUIDE**

```ruby
$ pip install playwright
$ playwright install 
```

```ruby
$ pip install -r requirements.txt
$ cd ./app/
$ streamlit run app.py
```

```toml
$ cd /app/.streamlit/config.toml

[server]
runOnSave = true

[logger]
level = "error"

[watchdog]
watcherType = "none"
```

### **ENVIRONMENT VARIABLES CONFIGURATION**

To ensure the application runs smoothly, configure the following environment variables in your `.env` file:

```plaintext
# API key for Maritalk integration
MARITALK_API_KEY=<your_maritalk_api_key>

# API key for LangSmith services
LANGSMITH_API_KEY=<your_langsmith_api_key>

# API key for Pinecone vector database
PINECONE_API_KEY=<your_pinecone_api_key>

# Optional: API key for Tavily services
TAVILY_API_KEY=<your_tavily_api_key>

# Enable LangSmith tracing for debugging and monitoring
LANGSMITH_TRACING=true
```

> [!NOTE]
> Replace `<your_*_api_key>` with the actual API keys provided by the respective services. Ensure these keys are kept secure and not exposed in public repositories.

---

### **AUTHORS**

[Giovane Iwamoto](https://github.com/GiovaneIwamoto) | [Matheus Tavares](https://github.com/mtguerson) | [Gustavo Vasconcelos](https://github.com/GustavoSVasconcelos)

