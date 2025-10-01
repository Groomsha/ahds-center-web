"""Допоміжні функції для телеграм бота."""

import logging
from typing import Dict, Any

# Built-in imports

# Third-party imports
from aiogram import Bot
from aiogram.types import Message

# Project imports


def setup_logging() -> None:
    """Налаштування конфігурації логування для бота."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_user_info(message: Message) -> Dict[str, Any]:
    """Отримати інформацію про користувача з повідомлення."""
    user = message.from_user
    if not user:
        return {}

    return {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'language_code': user.language_code
    }


async def send_test_message(bot: Bot, chat_id: int, message: str = "Бот запущено успішно! 🚀") -> bool:
    """Надіслати тестове повідомлення до вказаного чату."""
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        return True
    except Exception as e:
        logging.error(f"Failed to send test message: {e}")
        return False


def format_uptime(seconds: int) -> str:
    """Форматувати час роботи в зручний для читання формат."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}г {minutes}хв {seconds}с"