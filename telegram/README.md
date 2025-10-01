# Telegram Bot

Telegram бот для проекту Dark Tower, побудований на aiogram 3.13.1.

## Опис

Сучасний телеграм бот з асинхронною архітектурою та розширеною функціональністю.

## Функціональність

- Базові команди
- Автоматичне відправлення повідомлення при старті
- Логування подій

## Структура

- `bot.py` - Основний файл бота
- `utils.py` - Допоміжні функції
- `config.py` - Конфігурація бота

## Налаштування

1. Створіть бота через @BotFather в Telegram
2. Отримати токен бота
3. Встановити токен в .env файл
4. Запустити бота:
   - Директно: `python bot.py`
   - Через Django: `python manage.py run_telegram_bot`

## Змінні оточення

```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id
WEBHOOK_URL=https://yourdomain.com/webhook/
```

## Автозапуск

Бот може автоматично запускатися:
- Через systemd сервіс (файл `dark-tower-bot.service`)
- Через Django management команду: `python manage.py run_telegram_bot`
- Разом з Django сервером через supervisor

## Команди

- `/start` - Початок роботи з ботом
- `/help` - Допомога