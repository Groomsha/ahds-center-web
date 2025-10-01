"""Налаштування конфігурації для телеграм бота."""

import os
from typing import Optional

# Built-in imports

# Third-party imports
from decouple import config

# Project imports


class BotConfig:
    """Клас конфігурації бота."""

    def __init__(self) -> None:
        """Ініціалізувати конфігурацію бота з змінних оточення."""
        self.bot_token: str = str(config('BOT_TOKEN', default=''))
        self.admin_id: int = int(config('ADMIN_ID', default=0))
        self.debug: bool = bool(config('DEBUG', default=False))

    def validate(self) -> bool:
        """Перевірити параметри конфігурації."""
        if not self.bot_token:
            return False
        if not self.admin_id:
            return False
        return True


# Global config instance
bot_config = BotConfig()