# Ollama OpenRouter Proxy (Python)

**Languages:** [English](README.md) | [Русский](README_RU.md)

A lightweight Python proxy that lets Ollama-compatible apps use models from OpenRouter, including free models.

## Features

- Ollama-compatible API on `http://localhost:11434`
- Streaming chat responses
- Automatic OpenRouter model listing via `/api/tags`
- Model list caching for 10 minutes
- Vision-capable models work if supported by the selected app/model
- Simple terminal chat client for testing

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your OpenRouter API key

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=sk-or-v1-your-long-key
```

### 3. Start the proxy

```bash
python3 ollama_openrouter_proxy.py
```

The proxy listens on `http://localhost:11434`.

## Important

This project intentionally mimics the Ollama API on port `11434`.
That means it replaces the real Ollama server while it is running.

- If the proxy is running, regular `ollama pull`, `ollama run`, and `ollama list` will not work against the real Ollama daemon.
- If the real Ollama app is running, this proxy cannot start on port `11434`.

Use one of them at a time:

- Start the proxy when you want Ollama-compatible apps to use OpenRouter.
- Stop the proxy and run the real Ollama daemon when you want local Ollama models.

## Use With Ollama Apps

In any Ollama-compatible app, set:

- Base URL / Server Address: `http://localhost:11434`
- Model: choose any model returned by the proxy

Examples: Enchanted, Page Assist, Continue, Open WebUI.

## Terminal Chat Client

You can test the proxy directly from the terminal:

```bash
python3 chat.py
```

The client fetches available models from the proxy and sends chat requests through `/api/chat`.
When you use `change`, it shows `openrouter/free` plus a curated list of up to 15 known free models that are available right now.

## Useful Commands

Check the proxy status:

```bash
curl http://localhost:11434/ping
```

List all available models:

```bash
curl -s http://localhost:11434/api/tags
```

List only free models:

```bash
curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; print('\n'.join(sorted([m['name'] for m in json.load(sys.stdin)['models'] if ':free' in m['name']])))"
```

## Recommended Free Models

| Model | ID | Notes |
| :--- | :--- | :--- |
| OpenRouter Free Router | `openrouter/free` | Automatically picks an available free model |
| Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct:free` | Strong general-purpose model |
| Hermes 3 405B | `nousresearch/hermes-3-llama-3.1-405b:free` | Large and capable |
| DeepSeek R1 | `deepseek/deepseek-r1:free` | Good for reasoning and math |
| Gemini 2.0 Flash | `google/gemini-2.0-flash-exp:free` | Fast responses |
| Gemma 3 27B | `google/gemma-3-27b-it:free` | Vision support |
| Qwen 2.5 Coder | `qwen/qwen-2.5-coder-32b-instruct:free` | Good for code tasks |
| Mistral Small 3.1 | `mistralai/mistral-small-3.1-24b-instruct:free` | Balanced and efficient |
| Llama 3.2 3B | `meta-llama/llama-3.2-3b-instruct:free` | Lightweight general-purpose model |
| Llama 3.2 1B | `meta-llama/llama-3.2-1b-instruct:free` | Very small and fast |
| Gemma 2 9B | `google/gemma-2-9b-it:free` | Compact instruction model |
| Gemma 2 27B | `google/gemma-2-27b-it:free` | Larger Gemma variant |
| Qwen 2.5 72B | `qwen/qwen-2.5-72b-instruct:free` | Strong long-form model |
| Qwen 2.5 7B | `qwen/qwen-2.5-7b-instruct:free` | Smaller fast Qwen |
| Phi-3 Medium 128K | `microsoft/phi-3-medium-128k-instruct:free` | Long context model |
| Llama 3.1 Nemotron 70B | `nvidia/llama-3.1-nemotron-70b-instruct:free` | Nvidia-tuned large model |

## Troubleshooting

If you get `404 page not found` or port `11434` is busy:

1. Quit the original Ollama app if it is running.
2. Free the port manually if needed:

```bash
lsof -ti:11434 | xargs kill -9
```

3. Start the proxy again.

## Notes

- `openrouter/free` is a router provided by OpenRouter that automatically selects an available free model.
- Specific free models can be temporarily rate-limited, so `openrouter/free` is often the most reliable default choice.
