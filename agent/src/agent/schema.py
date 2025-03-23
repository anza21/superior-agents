from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

@dataclass
class Message:
    role: Role
    content: Optional[str] = None
    name: Optional[str] = None
    function_call: Optional[dict] = None

@dataclass
class Choice:
    message: Message
    finish_reason: str
    index: int

class TokenType(str, Enum):
    GENERATED = "generated"
    PROMPT = "prompt"
    CONTEXT = "context"

@dataclass
class ChatHistory:
    messages: List[Message]

    def get_latest_response(self):
        return self.messages[-1].content if self.messages else "No response"
