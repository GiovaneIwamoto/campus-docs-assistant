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
        self.logger.info(f"[#2D0856][AUTH][/#2D0856] LLM API Key: {llm_api_key}")
        self.logger.info(f"[#2D0856][AUTH][/#2D0856] Pinecone API Key: {pinecone_api_key}")
        self.logger.info(f"[#2D0856][AUTH][/#2D0856] Pinecone Index Name: {pinecone_index_name}\n")

    def chat_history(self, messages):
        self.logger.info(f"[#FFA500][CHAT HISTORY][/#FFA500] [#4169E1][All session state messages][/#4169E1]\n\n{format_chat_messages(messages)}\n\n\n\n")

    def tool_query(self, tool_action, query):
        self.logger.info(f"[#26F5C9][TOOL][/#26F5C9] [#4169E1][{tool_action}][/#4169E1] {query}\n")

    def tool_document(self, tool_action, retrieved_docs):
        self.logger.info(f"\n[#26F5C9][TOOL][/#26F5C9] [#4169E1][{tool_action}][/#4169E1] -> {len(retrieved_docs)}\n")

    def initializing(self):
        self.logger.info("[#18F54A][INITIALIZING][/#18F54A]\n")

    def trimmer(self, trimmer_info, trimmed_messages):
        self.logger.info(f"[#FFA500][TRIMMED MESSAGES][/#FFA500] [#4169E1][{trimmer_info}][/#4169E1]\n\n{format_chat_messages(trimmed_messages)}\n")
    
    def llm_decision(self, llm_action, llm_status):
        self.logger.info(f"[#6819B3][LLM][/#6819B3] [#4169E1][{llm_action}][/#4169E1] {llm_status}\n")

    def llm_response(self, llm_action, content):
        self.logger.info(f"[#6819B3][LLM][/#6819B3] [#4169E1][{llm_action}][/#4169E1]\n\n{content}\n")

    def llm_with_tools(self, llm_action):
        self.logger.info(f"[#6819B3][LLM TOOL][/#6819B3] [#4169E1][{llm_action}][/#4169E1]\n")

    def llm_tool_response(self, llm_info, messages):
        self.logger.info(f"[#6819B3][LLM TOOL][/#6819B3] [#4169E1][{llm_info}][/#4169E1]\n\n{format_chat_messages(messages)}\n")

    def llm_tool_last_message(self, llm_role_info, message):
        self.logger.info(f"[#6819B3][LLM TOOL][/#6819B3] [#4169E1][{llm_role_info}][/#4169E1] '{message}'\n")

    def parser_error(self, parser_status):
        self.logger.error(f"[#FF4F4F][PARSER][/#FF4F4F] {parser_status}\n")

    def parser_warning(self, parser_status):
        self.logger.warning(f"[#FF4F4F][PARSER][/#FF4F4F] {parser_status}\n")

    def error(self, error_type, exception):
        self.logger.error(f"{error_type} Error: {exception}\n")

    def warning(self, message):
        self.logger.warning(f"{message}\n")