![banner](https://github.com/user-attachments/assets/7b4565af-c0b4-4bfb-bdaf-9859347b7677)

### **INTRODUCTION**

This project aims to facilitate access for students of the Federal University of Mato Grosso do Sul (UFMS) to legal and academic documents, such as requirements for mandatory internships, enrollment policies, among others.

[![Icons](https://skillicons.dev/icons?i=aws,py,theme=dark)](https://skillicons.dev)

### **TOOLS AND TECHNOLOGIES**

[<img src="https://img.shields.io/badge/Serverless_Framework-ff5242?logo=serverless&logoColor=white">](https://www.serverless.com)
[<img src="https://img.shields.io/badge/AWS-CLI-fa8818?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/cli/)
[<img src="https://img.shields.io/badge/AWS-S3-2cae05?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/s3/)
[<img src="https://img.shields.io/badge/Amazon-DynamoDB-0a43e8?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/dynamodb/)
[<img src="https://img.shields.io/badge/Amazon-Bedrock-03ab9d?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/bedrock/)
[<img src="https://img.shields.io/badge/Amazon-Lex-03ab9d?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/transcribe/)

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

