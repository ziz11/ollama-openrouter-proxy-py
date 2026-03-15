import requests
import json
import sys

# Адрес вашего прокси
URL = "http://localhost:11434/api/chat"

def get_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        return [m['name'] for m in response.json()['models']]
    except:
        return []

def start_chat():
    models = get_models()
    
    # Модель по умолчанию
    default_model = "google/gemini-2.0-flash-001"
    if default_model not in models and models:
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
            print("\nДоступные модели:")
            for i, m in enumerate(models[:15]): # Показываем первые 15
                print(f"{i}: {m}")
            idx = input("\nВведите номер модели: ")
            try:
                current_model = models[int(idx)]
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
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "message" in chunk:
                            content = chunk["message"].get("content", "")
                            print(content, end="", flush=True)
                            full_response += content
                        elif "choices" in chunk: # Формат OpenRouter прямо
                            content = chunk["choices"][0]["delta"].get("content", "")
                            print(content, end="", flush=True)
                            full_response += content
            
            print("\n")
            # Сохраняем ответ AI в историю для контекста
            messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"\nОшибка: {e}\n")

if __name__ == "__main__":
    start_chat()
