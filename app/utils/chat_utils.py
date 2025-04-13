def format_chat_messages(messages: list) -> str:
    """
    Format a list of chat messages into a readable string representation.
    This function is utilized for debugging purposes to provide a clear view of the chat history by loggers.
    """
    formatted = []
    for msg in messages:
        role = msg.role if hasattr(msg, "role") else msg.__class__.__name__
        formatted.append(f"[{role}] {msg.content} (ID: {msg.id})")
    return "\n".join(formatted)