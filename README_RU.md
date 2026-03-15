# Ollama OpenRouter Proxy (Python)

**Языки:** [English](README.md) | [Русский](README_RU.md)

Легковесный Python-прокси, который позволяет Ollama-совместимым приложениям работать с моделями из OpenRouter, включая бесплатные.

## Возможности

- Ollama-совместимый API на `http://localhost:11434`
- Стриминг ответов в чате
- Автоматическая выдача списка моделей OpenRouter через `/api/tags`
- Кэширование списка моделей на 10 минут
- Поддержка vision-моделей, если это умеют выбранные приложение и модель
- Простой терминальный чат-клиент для проверки

## Быстрый старт

### 1. Установите зависимости

```bash
pip install -r requirements.txt
```

### 2. Добавьте OpenRouter API key

Создайте файл `.env` в корне проекта:

```env
OPENROUTER_API_KEY=sk-or-v1-ваш-длинный-ключ
```

### 3. Запустите прокси

```bash
python3 ollama_openrouter_proxy.py
```

Прокси будет слушать `http://localhost:11434`.

## Важно

Этот проект намеренно имитирует Ollama API на порту `11434`.
То есть во время работы он подменяет собой настоящий сервер Ollama.

- Если запущен прокси, обычные `ollama pull`, `ollama run` и `ollama list` не будут работать с настоящим демоном Ollama.
- Если запущен настоящий Ollama, этот прокси не сможет стартовать на порту `11434`.

Использовать их нужно по очереди:

- Запускайте прокси, когда хотите, чтобы Ollama-совместимые приложения работали через OpenRouter.
- Останавливайте прокси и запускайте настоящий Ollama, когда нужны локальные модели Ollama.

## Использование в Ollama-приложениях

В любом Ollama-совместимом приложении укажите:

- Base URL / Server Address: `http://localhost:11434`
- Model: выберите любую модель, которую отдаёт прокси

Примеры: Enchanted, Page Assist, Continue, Open WebUI.

## Терминальный чат-клиент

Для быстрой проверки можно запустить чат прямо из терминала:

```bash
python3 chat.py
```

Клиент получает список моделей через прокси и отправляет запросы в `/api/chat`.
При команде `change` он показывает `openrouter/free` и curated-список из максимум 15 известных бесплатных моделей, доступных в данный момент.

## Полезные команды

Проверить состояние прокси:

```bash
curl http://localhost:11434/ping
```

Получить список всех моделей:

```bash
curl -s http://localhost:11434/api/tags
```

Получить только бесплатные модели:

```bash
curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; print('\n'.join(sorted([m['name'] for m in json.load(sys.stdin)['models'] if ':free' in m['name']])))"
```

## Рекомендуемые бесплатные модели

| Модель | ID | Примечание |
| :--- | :--- | :--- |
| OpenRouter Free Router | `openrouter/free` | Автоматически выбирает доступную бесплатную модель |
| Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct:free` | Сильная универсальная модель |
| Hermes 3 405B | `nousresearch/hermes-3-llama-3.1-405b:free` | Большая и мощная |
| DeepSeek R1 | `deepseek/deepseek-r1:free` | Хороша для логики и математики |
| Gemini 2.0 Flash | `google/gemini-2.0-flash-exp:free` | Быстрые ответы |
| Gemma 3 27B | `google/gemma-3-27b-it:free` | Поддержка изображений |
| Qwen 2.5 Coder | `qwen/qwen-2.5-coder-32b-instruct:free` | Подходит для задач по коду |
| Mistral Small 3.1 | `mistralai/mistral-small-3.1-24b-instruct:free` | Сбалансированная и быстрая |
| Llama 3.2 3B | `meta-llama/llama-3.2-3b-instruct:free` | Лёгкая универсальная модель |
| Llama 3.2 1B | `meta-llama/llama-3.2-1b-instruct:free` | Очень маленькая и быстрая |
| Gemma 2 9B | `google/gemma-2-9b-it:free` | Компактная instruction-модель |
| Gemma 2 27B | `google/gemma-2-27b-it:free` | Более крупная версия Gemma |
| Qwen 2.5 72B | `qwen/qwen-2.5-72b-instruct:free` | Сильная модель для длинных ответов |
| Qwen 2.5 7B | `qwen/qwen-2.5-7b-instruct:free` | Меньшая и быстрая Qwen |
| Phi-3 Medium 128K | `microsoft/phi-3-medium-128k-instruct:free` | Модель с длинным контекстом |
| Llama 3.1 Nemotron 70B | `nvidia/llama-3.1-nemotron-70b-instruct:free` | Крупная Nvidia-версия |

## Решение проблем

Если видите `404 page not found` или порт `11434` занят:

1. Закройте оригинальный Ollama, если он запущен.
2. При необходимости освободите порт вручную:

```bash
lsof -ti:11434 | xargs kill -9
```

3. Запустите прокси снова.

## Примечания

- `openrouter/free` это роутер OpenRouter, который автоматически выбирает доступную бесплатную модель.
- Конкретные free-модели могут временно упираться в rate limit, поэтому `openrouter/free` часто самый надёжный вариант по умолчанию.
