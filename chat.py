import requests
import json
import sys
from requests.exceptions import ChunkedEncodingError

# Адрес вашего прокси
URL = "http://localhost:11434/api/chat"
RECOMMENDED_FREE_MODELS = [
    "openrouter/free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "deepseek/deepseek-r1:free",
    "google/gemini-2.0-flash-exp:free",
    "google/gemma-3-27b-it:free",
    "qwen/qwen-2.5-coder-32b-instruct:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "meta-llama/llama-3.2-1b-instruct:free",
    "google/gemma-2-9b-it:free",
    "google/gemma-2-27b-it:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
    "microsoft/phi-3-medium-128k-instruct:free",
    "nvidia/llama-3.1-nemotron-70b-instruct:free",
]


def parse_stream_line(line):
    if isinstance(line, bytes):
        line = line.decode("utf-8", errors="ignore")

    line = line.strip()
    if not line:
        return None

    if line.startswith(":") or line.startswith("event:"):
        return None

    if line.startswith("data:"):
        line = line[5:].strip()

    if line == "[DONE]":
        return None

    if not line.startswith("{"):
        return None

    return json.loads(line)


def format_api_error(error_payload):
    if isinstance(error_payload, dict):
        error = error_payload.get("error", error_payload)
        if isinstance(error, dict):
            code = error.get("code")
            message = error.get("message", "Unknown API error")
            metadata = error.get("metadata", {})
            raw = metadata.get("raw")

            if code == 429:
                if raw:
                    return f"Модель временно недоступна из-за rate limit: {raw}\nПопробуйте позже или выберите другую модель через 'change'."
                return "Модель временно недоступна из-за rate limit. Попробуйте позже или выберите другую модель через 'change'."

            if raw:
                return f"{message}: {raw}"
            return str(message)

    return str(error_payload)

def get_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        return [m['name'] for m in response.json()['models']]
    except:
        return []


def get_recommended_models(models):
    available = set(models)
    recommended = []
    for model in RECOMMENDED_FREE_MODELS:
        if model == "openrouter/free" or model in available:
            recommended.append(model)
    if recommended:
        return recommended
    return [model for model in models if model.endswith(":free")]

def start_chat():
    models = get_models()
    selectable_models = get_recommended_models(models)
    
    # Модель по умолчанию
    default_model = "openrouter/free"
    if default_model not in selectable_models and selectable_models:
        default_model = selectable_models[0]
    elif not selectable_models and models:
        default_model = models[0]

    print(f"\n--- Чат с OpenRouter (через Ollama Proxy) ---")
    print(f"Используемая модель: {default_model}")
    print(f"Введите 'exit' для выхода или 'change' для смены модели.\n")

    current_model = default_model
    messages = []

    while True:
        user_input = input("You > ").strip()
        
        if not user_input:
            continue
        if user_input.lower() == 'exit':
            break
        if user_input.lower() == 'change':
            selectable_models = get_recommended_models(get_models())
            if not selectable_models:
                print("\nНет доступных рекомендованных бесплатных моделей.\n")
                continue

            print("\nРекомендованные бесплатные модели:")
            for i, m in enumerate(selectable_models):
                print(f"{i}: {m}")
            idx = input("\nВведите номер модели: ")
            try:
                current_model = selectable_models[int(idx)]
                print(f"Модель изменена на: {current_model}\n")
                messages = [] # Сбрасываем контекст при смене модели
                continue
            except:
                print("Ошибка выбора, остаемся на прежней.\n")
                continue

        # Добавляем сообщение пользователя в историю
        messages.append({"role": "user", "content": user_input})
        
        payload = {
            "model": current_model,
            "messages": messages,
            "stream": True
        }

        print("AI  > ", end="", flush=True)
        
        full_response = ""
        try:
            with requests.post(URL, json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = parse_stream_line(line)
                        except json.JSONDecodeError:
                            raw_line = line.decode("utf-8", errors="ignore") if isinstance(line, bytes) else str(line)
                            raise RuntimeError(f"Некорректная строка стрима: {raw_line[:200]}")
                        if not chunk:
                            continue
                        if "error" in chunk:
                            raise RuntimeError(format_api_error(chunk))
                        if "message" in chunk:
                            content = chunk["message"].get("content", "")
                            print(content, end="", flush=True)
                            full_response += content
                        elif "choices" in chunk: # Формат OpenRouter прямо
                            delta = chunk["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                print(content, end="", flush=True)
                                full_response += content
            
            print("\n")
            if full_response:
                # Сохраняем ответ AI в историю для контекста
                messages.append({"role": "assistant", "content": full_response})
            else:
                print("Пустой ответ от модели.\n")
            
        except ChunkedEncodingError:
            if full_response:
                messages.append({"role": "assistant", "content": full_response})
                print("\n\nПоток ответа завершился раньше времени, частичный ответ сохранен.\n")
            else:
                print("\nОшибка: поток ответа завершился раньше времени.\n")
        except Exception as e:
            print(f"\nОшибка: {e}\n")

if __name__ == "__main__":
    start_chat()
