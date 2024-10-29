# UFMS DOCUMENT BOT

### **INTRODUÇÃO**

Chatbot UFMS para Solicitação de Documentos Oficiais

Este projeto visa facilitar o acesso de estudantes da Universidade Federal de Mato Grosso do Sul (UFMS) a documentos legais e acadêmicos, como os requisitos para estágio obrigatório, políticas de matrícula, entre outros. O chatbot, integrado com o Amazon Lex V2 e a plataforma Telegram, permite que os alunos solicitem informações de forma rápida e eficiente, enviando respostas automáticas com os documentos solicitados.

[![Icons](https://skillicons.dev/icons?i=aws,py,theme=dark)](https://skillicons.dev)

---

### **ARQUITETURA**

---

### **FUNCIONALIDADES**

---

### **FERRAMENTAS E TECNOLOGIAS**

[<img src="https://img.shields.io/badge/Serverless_Framework-ff5242?logo=serverless&logoColor=white">](https://www.serverless.com)
[<img src="https://img.shields.io/badge/AWS-CLI-fa8818?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/pt/cli/)
[<img src="https://img.shields.io/badge/AWS-S3-2cae05?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/pt/s3/)
[<img src="https://img.shields.io/badge/Amazon-DynamoDB-0a43e8?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/pt/pm/dynamodb/)
[<img src="https://img.shields.io/badge/Amazon-Bedrock-03ab9d?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/pt/bedrock/)
[<img src="https://img.shields.io/badge/Amazon-Lex-03ab9d?logo=amazon-web-services&logoColor=ffff&labelColor=232F3E">](https://aws.amazon.com/pt/transcribe/)

---

### **GUIA DE INSTALAÇÃO**

- Clone o repositório e navegue até a branch mencionada.

```ruby
$ git clone https://github.com/GiovaneIwamoto/ufms-document-bot
$ cd ufms-document-bot
$ git checkout main
```

- Configure o framework Serverless e as credenciais AWS.

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

- Navegue até a pasta onde se encontra o arquivo Serverless e realize o deploy da aplicação.

```ruby
$ cd src/backend
$ serverless deploy
```

---

### **AUTORES**

[Giovane Iwamoto](https://github.com/GiovaneIwamoto) | [Matheus Tavares](https://github.com/mtguerson) | [Gustavo Vasconcelos](https://github.com/GustavoSVasconcelos)
