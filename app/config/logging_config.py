import logging
from rich.logging import RichHandler
from utils.chat_formatter import format_chat_messages

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(message)s",handlers=[RichHandler(rich_tracebacks=True, markup=True)])
    logger = logging.getLogger(__name__)
    return logger

class EnhancedLogger:
    def __init__(self, logger):
        self.logger = logger

    def auth(self, llm_api_key, pinecone_api_key, pinecone_index_name):
        self.logger.info(f"\n[#2D0856][AUTH][/#2D0856] LLM API Key: {llm_api_key}")
        self.logger.info(f"[#2D0856][AUTH][/#2D0856] Pinecone API Key: {pinecone_api_key}")
        self.logger.info(f"[#2D0856][AUTH][/#2D0856] Pinecone Index Name: {pinecone_index_name}\n")

    def chat_history(self, messages):
        self.logger.info(f"[#FFA500][CHAT HISTORY][/#FFA500] [#4169E1][All session state messages][/#4169E1]\n\n{format_chat_messages(messages)}\n\n\n")

    def tool(self, tool_action, tool_args):
        self.logger.info(f"[#26F5C9][TOOL][/#26F5C9] [#4169E1][{tool_action}][/#4169E1] {tool_args}\n")

    def error(self, error_type, exception):
        self.logger.error(f"{error_type} Error: {exception}\n")

    def warning(self, message):
        self.logger.warning(f"{message}\n")