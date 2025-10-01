"""Основна програма телеграм бота."""

import asyncio
import logging
from typing import Optional

# Built-in imports

# Third-party imports
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Project imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import bot_config
from utils import setup_logging, send_test_message


class TelegramBot:
    """Основний клас телеграм бота."""

    def __init__(self) -> None:
        """Ініціалізувати бота."""
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self._running = False

    def setup(self) -> None:
        """Налаштувати бота та диспетчер."""
        if not bot_config.validate():
            raise ValueError("Invalid bot configuration")

        from aiogram.client.default import DefaultBotProperties
        self.bot = Bot(
            token=bot_config.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        self.dp = Dispatcher()

        # Register basic handlers
        self.dp.message.register(self.cmd_start, Command("start"))
        self.dp.message.register(self.cmd_help, Command("help"))

        # Setup logging
        setup_logging()

    async def cmd_start(self, message: Message) -> None:
        """Обробити команду /start."""
        await message.reply(
            "🤖 Бот запущено!\n\n"
            "Використовуйте /help для отримання довідки."
        )

    async def cmd_help(self, message: Message) -> None:
        """Обробити команду /help."""
        await message.reply(
            "🆘 Допомога\n\n"
            "Доступні команди:\n"
            "/start - Початок роботи\n"
            "/help - Ця довідка"
        )

    async def send_startup_message(self) -> None:
        """Надіслати повідомлення про запуск адміністратору."""
        if self.bot and bot_config.admin_id:
            success = await send_test_message(
                self.bot,
                bot_config.admin_id,
                "🤖 Бот запущено успішно!"
            )

            if success:
                logging.info("Startup message sent to admin")
            else:
                logging.error("Failed to send startup message")

    async def start_polling(self) -> None:
        """Запустити опитування бота."""
        if not self.bot or not self.dp:
            raise RuntimeError("Bot not properly initialized")

        self._running = True
        logging.info("Starting bot polling...")

        await self.send_startup_message()

        try:
            await self.dp.start_polling(
                self.bot,
                allowed_updates=["message"]
            )
        except Exception as e:
            logging.error(f"Polling error: {e}")
            raise
        finally:
            self._running = False

    async def stop(self) -> None:
        """Зупинити бота."""
        if self.bot and self._running:
            await self.bot.session.close()
            self._running = False
            logging.info("Bot stopped")

    def is_running(self) -> bool:
        """Перевірити чи бот запущено."""
        return self._running


# Global bot instance
telegram_bot = TelegramBot()


async def main() -> None:
    """Основна точка входу для бота."""
    try:
        telegram_bot.setup()
        await telegram_bot.start_polling()
    except KeyboardInterrupt:
        logging.info("Bot interrupted by user")
    except Exception as e:
        logging.error(f"Bot error: {e}")
    finally:
        await telegram_bot.stop()


if __name__ == "__main__":
    asyncio.run(main())