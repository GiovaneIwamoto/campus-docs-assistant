def format_chat_messages(messages: list) -> str:
    """
    Format a list of chat messages into a readable, colorized string.
    
    Args:
        messages (list): List of chat message objects.
    
    Returns:
        str: Formatted string with color codes for different message roles.
    """

    role_colors = {
        "HumanMessage": "bold red",
        "AIMessage": "bold yellow",
        "SystemMessage": "bold magenta",
        "ToolMessage": "blue",
        "ChatMessage": "green",
        }

    formatted = []
    for msg in messages:
        role = msg.__class__.__name__
        color = role_colors.get(role, "white")
        role_tag = f"[{color}][{role}] [/]"
        formatted.append(f"{role_tag} {msg.content.strip()}")

    return "\n".join(formatted)
