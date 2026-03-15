# Ollama OpenRouter Proxy (Python)

Легковесный прокси-сервер на Python, который позволяет использовать любые модели **OpenRouter** (включая новейшие бесплатные) в приложениях, предназначенных для **Ollama** (Enchanted, Page Assist, Continue, Open WebUI и др.).

## 🚀 Основные возможности
- **Полная совместимость с Ollama API**: Работает как "дроп-ин" замена на порту `11434`.
- **Поддержка стриминга (Streaming)**: Текст появляется по мере генерации, как в ChatGPT.
- **Автоматический список моделей**: Прокси сам подтягивает все доступные модели из OpenRouter.
- **Кэширование**: Список моделей обновляется раз в 10 минут, не замедляя работу интерфейса.
- **Поддержка Vision моделей**: Работает с моделями, понимающими изображения (например, Gemma 3).

## 🛠 Быстрая настройка

### 1. Подготовка ключа
Создайте файл `.env` в папке проекта и добавьте ваш API-ключ от [OpenRouter](https://openrouter.ai/keys):
```env
OPENROUTER_API_KEY=sk-or-v1-ваш-длинный-ключ
```

### 2. Запуск сервера
Используйте готовый скрипт в вашей папке Documents:
```bash
~/Documents/run_ollama_proxy.sh
```
Сервер будет доступен по адресу: `http://localhost:11434`

## 📱 Как использовать в приложениях
В любом Ollama-совместимом приложении укажите:
- **Base URL / Server Address**: `http://localhost:11434`
- **Model**: Выберите из выпадающего списка (прокси сам отдаст все модели OpenRouter).

## 🎁 Актуальные бесплатные модели (Free Models)
Просто скопируйте ID и вставьте в поле выбора модели:

| Название модели | ID для использования | Особенности |
| :--- | :--- | :--- |
| **Llama 3.3 70B** | `meta-llama/llama-3.3-70b-instruct:free` | Самая мощная универсальная |
| **Hermes 3 405B** | `nousresearch/hermes-3-llama-3.1-405b:free` | Огромная и очень умная |
| **DeepSeek R1** | `deepseek/deepseek-r1:free` | Лучшая для логики и математики |
| **Gemini 2.0 Flash** | `google/gemini-2.0-flash-exp:free` | Сверхбыстрая от Google |
| **Gemma 3 27B** | `google/gemma-3-27b-it:free` | Новинка, понимает изображения |
| **Qwen 2.5 Coder** | `qwen/qwen-2.5-coder-32b-instruct:free` | Идеальна для программирования |
| **Mistral Small** | `mistralai/mistral-small-3.1-24b-instruct:free` | Сбалансированная и быстрая |

## 🔍 Полезные команды для проверки

**Проверка связи с прокси:**
```bash
curl http://localhost:11434/ping
```

**Получить список всех бесплатных моделей:**
```bash
curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; print('\n'.join(sorted([m['name'] for m in json.load(sys.stdin)['models'] if ':free' in m['name']])))"
```

**Тестовый чат через терминал:**
```bash
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "google/gemini-2.0-flash-001", "messages": [{"role": "user", "content": "Привет!"}], "stream": false}'
```

## ⚠️ Решение проблем
Если вы видите ошибку `404 page not found` или порт занят:
1. Выключите оригинальную Ollama (иконка в трее -> Quit).
2. Если не помогает, очистите порт вручную:
   ```bash
   lsof -ti:11434 | xargs kill -9
   ```
3. Запустите прокси снова.

---
*Приятного использования!*
