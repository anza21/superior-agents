from typing import List, Optional, Tuple
from loguru import logger

from src.agent.schema import Message, TokenType, ChatHistory
from src.genner.Base import Genner


class DeepseekGenner(Genner):
    def __init__(self, client, config, stream_fn=None, summarizer=False):
        self.client = client
        self.config = config
        self.stream_fn = stream_fn
        self.summarizer = summarizer

    def set_do_stream(self, val: bool):
        self.stream_fn = None if not val else self.stream_fn

    def ch_completion(
        self, messages: List[Message], functions: Optional[List[dict]] = None
    ) -> Tuple[str, TokenType]:
        if isinstance(messages, ChatHistory):
            messages = messages.messages

        stream_ = None
        try:
            stream_ = self._stream_response(messages, functions)
            result = ""
            for token, token_type in stream_:
                result += token
            return result, TokenType.GENERATED

        except Exception as e:
            logger.exception(
                f"DeepseekGenner.ch_completion: Unexpected error: {e}"
            )
            return "print('error')", TokenType.GENERATED

    def _stream_response(self, messages, functions):
        return self.client.create_chat_completion_stream(
            messages=messages,
            providers=["openrouter"],
            temperature=self.config.temperature,
            model=self.config.model,
            max_tokens=1024,
        )

    def generate_code(self, messages: List[Message]) -> Tuple[str, TokenType]:
        return self.ch_completion(messages)

    def extract_code(self, text: str) -> str:
        return text

    def generate_list(self, messages: List[Message]) -> Tuple[List[str], TokenType]:
        return ["item1", "item2"], TokenType.GENERATED

    def extract_list(self, text: str) -> List[str]:
        return text.splitlines()
