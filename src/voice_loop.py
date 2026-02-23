import asyncio
import threading
from .asr import listen
from .llm import LLM
from .tts import speak

async def main():
    llm = LLM()
    stop_event = threading.Event()
    print('[VOICE] Ready – speak something (Ctrl‑C to quit)')
    while True:
        # 1️⃣ Capture speech
        user_text = await asyncio.to_thread(listen, stop_event)
        if not user_text:
            continue
        print(f'[USER] {user_text}')
        # 2️⃣ Ask LLM
        response = await llm.infer(user_text)
        print(f'[LLM] {response}')
        # 3️⃣ Speak back
        await asyncio.to_thread(speak, response)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n[VOICE] Bye!')
