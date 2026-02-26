"""Model abstraction layer for LLM back‑ends.

Each concrete implementation must provide an ``async infer(prompt: str) -> str``
method.  The classes are deliberately lightweight – they only wrap the HTTP
call (or a stub) necessary for the selected provider.
"""

from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    async def infer(self, prompt: str) -> str:
        """Return the model's response for *prompt*.
        """
        raise NotImplementedError
