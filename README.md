# AHDS Center Web

Веб-проект Dark Tower з Django та Telegram ботом.

## Опис

Проект складається з веб-додатку на Django та Telegram бота, побудованого на aiogram.

## Структура проекту

- `core/` - Базові компоненти та утиліти
- `hard/` - Основний Django додаток
- `telegram/` - Telegram бот на aiogram
- `www/` - Основні налаштування Django проекту

## Технології

- **Backend**: Django 5.2.7
- **Telegram Bot**: aiogram 3.13.1
- **Конфігурація**: python-decouple 3.8
- **База даних**: SQLite

## Встановлення та налаштування

### 1. Клонування та залежності
```bash
git clone <repository-url>
cd ahds-center-web
pip install -r requirements.txt
```

### 2. Налаштування бази даних
```bash
python manage.py migrate
```

### 3. Налаштування Telegram бота
```bash
# Створіть бота через @BotFather в Telegram
# Створіть .env файл у папці telegram/ з токеном:
echo "BOT_TOKEN=your_bot_token_here" > telegram/.env
echo "ADMIN_ID=your_telegram_id" >> telegram/.env
```

### 📋 Аргументи run_django_bot.py скрипта

Основний скрипт `run_django_bot.py` підтримує наступні аргументи:

```bash
python run_django_bot.py [АРГУМЕНТИ ДЛЯ DJANGO]

Аргументи:
  --no-bot              Запуск тільки Django сервера без бота
  django_args           Аргументи, які передаються Django командам

Приклади:
  python run_django_bot.py --no-bot runserver 0.0.0.0:8000
  python run_django_bot.py runserver --settings=www.settings.production
  python run_django_bot.py --no-bot migrate
```

## Запуск проекту

### 🚀 Швидкий запуск (рекомендовано)

```bash
# Запуск Django сервера з Telegram ботом (основний спосіб)
python run_django_bot.py

# Або з налаштуванням хоста та порту
python run_django_bot.py runserver 0.0.0.0:8000
```

### 🔧 Детальні налаштування запуску

#### Запуск з ботом (рекомендовано):
```bash
# Базовий запуск Django + Telegram бот
python run_django_bot.py

# З кастомним хостом та портом
python run_django_bot.py runserver 0.0.0.0:8000

# З додатковими аргументами Django
python run_django_bot.py runserver --settings=www.settings.production

# В режимі розробки з відлагодженням
DJANGO_DEBUG=True python run_django_bot.py
```

#### Запуск без бота:
```bash
# Тільки Django веб-сервер
python run_django_bot.py --no-bot

# З кастомними налаштуваннями
python run_django_bot.py --no-bot runserver 0.0.0.0:8000

# В production режимі
python run_django_bot.py --no-bot runserver 0.0.0.0:8000 --noreload
```

### 🔄 Альтернативні способи запуску

#### Через Django management команди:
```bash
# Запуск Django сервера з ботом
python manage.py run_telegram_bot

# З кастомними аргументами
python manage.py run_telegram_bot --host=0.0.0.0 --port=8000
```

#### Окремі компоненти:
```bash
# Тільки Django веб-сервер
python manage.py runserver

# Тільки Django веб-сервер з налаштуваннями
python manage.py runserver 0.0.0.0:8000

# Тільки Telegram бот
python telegram/bot.py
```

### 🚀 Production режим

#### Через Gunicorn + Django:
```bash
pip install gunicorn
gunicorn www.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

#### Через run_django_bot.py скрипт:
```bash
# Production режим без бота
python run_django_bot.py --no-bot runserver 0.0.0.0:8000 --noreload

# З ботом в production
python run_django_bot.py runserver 0.0.0.0:8000 --noreload
```

#### Через Django development сервер:
```bash
python manage.py runserver 0.0.0.0:8000 --noreload
```

#### Автозапуск через systemd:
```bash
# Скопіюйте та активуйте сервіс
sudo cp telegram/dark-tower-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dark-tower-bot
sudo systemctl start dark-tower-bot
```

### ✅ Перевірка статусу

#### Django система:
```bash
python manage.py check
python manage.py showmigrations
```

#### Системні сервіси:
```bash
sudo systemctl status dark-tower-bot
journalctl -u dark-tower-bot -f
```

## Додаткові команди

### Управління міграціями:
```bash
# Створити нові міграції
python manage.py makemigrations

# Застосувати міграції
python manage.py migrate

# Скасувати останню міграцію
python manage.py migrate <app_name> <migration_number>
```

### Суперкористувач Django:
```bash
python manage.py createsuperuser
```

### Збір статичних файлів:
```bash
python manage.py collectstatic
```

## Автозапуск та розгортання

Проект підтримує кілька варіантів автоматичного запуску та розгортання:

### Systemd сервіс
Проект містить готовий systemd сервіс для автоматичного запуску Telegram бота:
```bash
sudo cp telegram/dark-tower-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dark-tower-bot
sudo systemctl start dark-tower-bot
```

### Docker (рекомендовано для продакшену)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate

# Запуск Django з ботом (основний варіант)
CMD ["python", "run_django_bot.py"]

# Або тільки Django без бота
# CMD ["python", "run_django_bot.py", "--no-bot", "runserver", "0.0.0.0:8000"]
```

### Supervisor
```ini
[program:dark-tower]
command=python run_django_bot.py
directory=/path/to/ahds-center-web
autostart=true
autorestart=true
stderr_logfile=/var/log/dark-tower.err.log
stdout_logfile=/var/log/dark-tower.out.log
user=www-data
environment=DJANGO_SETTINGS_MODULE=www.settings.production
```

### Docker Compose (повний стек)
```yaml
version: '3.8'
services:
  web:
    build: .
    command: python run_django_bot.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - ./db.sqlite3:/app/db.sqlite3
    environment:
      - DJANGO_DEBUG=False
```