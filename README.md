![banner](https://github.com/user-attachments/assets/7b4565af-c0b4-4bfb-bdaf-9859347b7677)

### **INTRODUCTION**

UFMS Chatbot for Requesting Official Documents

This project aims to facilitate access for students of the Federal University of Mato Grosso do Sul (UFMS) to legal and academic documents, such as requirements for mandatory internships, enrollment policies, among others.

[![Icons](https://skillicons.dev/icons?i=aws,py,theme=dark)](https://skillicons.dev)

---

### **ARCHITECTURE**

---

### **FEATURES**

---

### **TOOLS AND TECHNOLOGIES**

[<img src="https://img.shields.io/badge/Serverless_Framework-ff5242?logo=serverless&logoColor=white">](https://www.serverless.com)
[<img src="https://img.shields.io/badge/AWS-CLI-fa8818?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/cli/)
[<img src="https://img.shields.io/badge/AWS-S3-2cae05?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/s3/)
[<img src="https://img.shields.io/badge/Amazon-DynamoDB-0a43e8?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/dynamodb/)
[<img src="https://img.shields.io/badge/Amazon-Bedrock-03ab9d?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/bedrock/)
[<img src="https://img.shields.io/badge/Amazon-Lex-03ab9d?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/transcribe/)

---

### **INSTALLATION GUIDE STREAMLIT APP**

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

### **INSTALLATION GUIDE**

- Clone the repository and navigate to the mentioned branch.

```ruby
$ git clone https://github.com/GiovaneIwamoto/campus-docs-assistant
$ cd ufms-document-bot
$ git checkout main
```

- Install the required dependencies.
```ruby
$ pip install -r requirements.txt
```

- Configure the Serverless framework and AWS credentials.

```ruby
$ serverless
```

```ruby
$ aws configure
AWS Access Key ID [None]: EXAMPLEKEYID
AWS Secret Access Key [None]: SECRETACCESSKEYEXAMPLE
Default region name [None]: us-east-1
Default output format [None]: ENTER
```

- Navigate to the folder containing the Serverless file and deploy the application.

```ruby
$ cd src/backend
$ serverless deploy
```

---

### **AUTHORS**

[Giovane Iwamoto](https://github.com/GiovaneIwamoto) | [Matheus Tavares](https://github.com/mtguerson) | [Gustavo Vasconcelos](https://github.com/GustavoSVasconcelos)

