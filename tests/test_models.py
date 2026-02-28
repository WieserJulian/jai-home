import asyncio
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path (tests/__init__.py already does this)

import src.models.vllm as vllm_mod
import src.models.openai as openai_mod
import src.models.anthropic as anthropic_mod


def test_vllm_client(httpx_mock):
    # Mock the VLLM endpoint
    url = "http://localhost:8000/v1/chat/completions"
    httpx_mock.add_response(
        method="POST",
        url=url,
        json={"choices": [{"message": {"content": "VLLM reply"}}]},
        status_code=200,
    )
    client = vllm_mod.VLLMClient()
    result = asyncio.run(client.infer("Hello"))
    assert result == "VLLM reply"


def test_openai_client(httpx_mock):
    # Mock the OpenAI endpoint – ensure AUTH header is accepted
    url = "https://api.openai.com/v1/chat/completions"
    httpx_mock.add_response(
        method="POST",
        url=url,
        json={"choices": [{"message": {"content": "OpenAI reply"}}]},
        status_code=200,
    )
    # Provide a dummy API key via env
    os.environ["OPENAI_API_KEY"] = "test-key"
    client = openai_mod.OpenAIClient()
    result = asyncio.run(client.infer("Hi"))
    assert result == "OpenAI reply"
    # Clean up env
    del os.environ["OPENAI_API_KEY"]


def test_anthropic_client(httpx_mock):
    url = "https://api.anthropic.com/v1/messages"
    httpx_mock.add_response(
        method="POST",
        url=url,
        json={"content": [{"text": "Anthropic reply"}]},
        status_code=200,
    )
    os.environ["ANTHROPIC_API_KEY"] = "anthropic-key"
    client = anthropic_mod.AnthropicClient()
    result = asyncio.run(client.infer("Hey"))
    assert result == "Anthropic reply"
    del os.environ["ANTHROPIC_API_KEY"]
