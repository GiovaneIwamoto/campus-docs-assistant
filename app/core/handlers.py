from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """
        Append new tokens to the response and update the UI dynamically.
        """
        self.text += token
        self.container.markdown(self.text)