"""Copilot stub client.

Microsoft Copilot does not have a public API yet, so this class provides a
placeholder implementation that simply returns a formatted string.
It allows the rest of the codebase to treat ``copilot`` as a valid backend
without external dependencies.
"""

from . import BaseLLM

class CopilotClient(BaseLLM):
    def __init__(self, model: str = "copilot"):
        self.model = model

    async def infer(self, prompt: str) -> str:
        # Placeholder behavior – echo the prompt with a note.
        return f"[Copilot placeholder] Received: {prompt}"
