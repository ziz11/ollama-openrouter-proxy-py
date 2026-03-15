import os
import time
import requests
from flask import Flask, request, jsonify, Response, stream_with_context
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

app = Flask(__name__)

# Настройки OpenRouter - Проверяем URL (согласно документации OpenRouter)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

# Кэш для моделей
models_cache = {"data": None, "last_updated": 0}
CACHE_TTL = 600

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok", 
        "message": "Proxy is alive!", 
        "key_loaded": bool(OPENROUTER_API_KEY),
        "key_preview": f"{OPENROUTER_API_KEY[:6]}***" if OPENROUTER_API_KEY else "none"
    })

def get_openrouter_models():
    now = time.time()
    if models_cache["data"] and (now - models_cache["last_updated"] < CACHE_TTL):
        return models_cache["data"]

    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"} if OPENROUTER_API_KEY else {}
    try:
        response = requests.get(OPENROUTER_MODELS_URL, headers=headers, timeout=10)
        response.raise_for_status()
        raw_models = response.json().get("data", [])
        ollama_models = []
        for m in raw_models:
            model_id = m.get("id")
            ollama_models.append({
                "name": model_id,
                "model": model_id,
                "modified_at": "2024-03-15T00:00:00Z",
                "details": {"family": "openrouter"}
            })
        models_cache["data"] = ollama_models
        models_cache["last_updated"] = now
        return ollama_models
    except Exception as e:
        print(f"DEBUG MODELS ERROR: {e}")
        return [{"name": "openrouter/error", "model": "openrouter/error", "details": {"family": "error"}}]

@app.route("/api/tags", methods=["GET"])
def tags():
    return jsonify({"models": get_openrouter_models()})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    is_streaming = data.get("stream", False)
    
    # Очень важно: OpenRouter требует эти заголовки для корректной работы
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:11434", # Опционально, но рекомендуется
        "X-Title": "Ollama Python Proxy"          # Опционально, но рекомендуется
    }

    try:
        if is_streaming:
            def generate():
                with requests.post(OPENROUTER_CHAT_URL, json=data, headers=headers, stream=True) as response:
                    if response.status_code != 200:
                        yield json.dumps({"error": response.text}).encode() + b"\n"
                        return
                    for line in response.iter_lines():
                        if line:
                            yield line + b"\n"
            return Response(stream_with_context(generate()), content_type='application/x-ndjson')
        else:
            response = requests.post(OPENROUTER_CHAT_URL, json=data, headers=headers)
            if response.status_code != 200:
                print(f"DEBUG CHAT ERROR RESPONSE: {response.text}")
                return jsonify({"error": f"OpenRouter error {response.status_code}: {response.text}"}), response.status_code
            return jsonify(response.json())
    except Exception as e:
        print(f"DEBUG CHAT EXCEPTION: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print(f"Starting proxy on http://0.0.0.0:11434")
    app.run(host="0.0.0.0", port=11434, debug=True)
