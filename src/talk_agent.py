"""Simple talk agent – reads user input from stdin and forwards it to the LLM.

Usage::

    python -m src.talk_agent

The script runs an async loop, sends each line to the configured backend and
prints the response.  It exits on EOF (Ctrl‑D) or when the user types ``exit``.
"""

import asyncio
import sys
from .llm import LLM

async def main():
    llm = LLM()
    print("JAI Talk Agent – type your prompt (or 'exit' to quit)")
    while True:
        try:
            prompt = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        except Exception:
            break
        if not prompt:
            break  # EOF
        prompt = prompt.rstrip("\n")
        if prompt.lower() in {"exit", "quit"}:
            break
        response = await llm.infer(prompt)
        print(f"JAI > {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
