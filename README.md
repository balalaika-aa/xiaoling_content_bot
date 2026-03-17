# Контент-ассистент @amagyrova

## Деплой на Railway

### Шаг 1 — GitHub
1. Зайди на github.com
2. Нажми "New repository"
3. Назови: `elena-content-bot`
4. Нажми "Create repository"
5. Загрузи три файла: bot.py, requirements.txt, Procfile

### Шаг 2 — Railway
1. Зайди на railway.app
2. Нажми "New Project"
3. Выбери "Deploy from GitHub repo"
4. Выбери `elena-content-bot`
5. Нажми "Deploy Now"

### Шаг 3 — Переменные окружения
В Railway зайди в свой проект → Variables → добавь:

```
TELEGRAM_TOKEN = твой_токен_от_BotFather
ANTHROPIC_API_KEY = твой_ключ_от_Anthropic
```

### Шаг 4 — API ключ Anthropic
1. Зайди на console.anthropic.com
2. Зарегистрируйся
3. API Keys → Create Key
4. Скопируй ключ и вставь в Railway

### Готово!
Напиши боту /start и проверь.

## Использование
- /start — начать создание текста
- /cancel — отменить
- Переписать 🔄 — новый вариант с теми же данными
- Новый текст ✨ — начать заново
