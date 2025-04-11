from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that provides information about campus resources."),
    MessagesPlaceholder(variable_name="messages"),
])
