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

        # ✅ Αν είναι string, σημαίνει ότι κάτι πήγε στραβά πριν από εδώ!
        if isinstance(messages, str):
            logger.error(f"[Deepseek] ❌ ERROR: Received string instead of list! messages={messages}")
            return "error", TokenType.GENERATED

        # ✅ Αν είναι ChatHistory, το μετατρέπουμε σε λίστα από dictionaries
        if isinstance(messages, ChatHistory):
            messages = [{"role": msg.role, "content": msg.content} for msg in messages.messages]

        # ✅ Αν δεν είναι λίστα, κάνουμε έναν ακόμα έλεγχο
        if not isinstance(messages, list):
            logger.error(f"[Deepseek] ❌ ERROR: Invalid type for messages: {type(messages)}")
            return "error", TokenType.GENERATED

        logger.info("[Deepseek] ✅ Sending request with correct format...")

        # ✅ Επεξεργασία απάντησης από το AI
        try:
            response = self._stream_response(messages, functions)
            full_response = "".join([token for token, _ in response])  # Συνένωση των tokens
            return full_response, TokenType.GENERATED

        except Exception as e:
            logger.error(f"[Deepseek] ❌ ERROR: Exception while generating response: {e}")
            return "error", TokenType.GENERATED


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
