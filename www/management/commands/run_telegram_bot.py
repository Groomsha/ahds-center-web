"""Команда Django для запуску телеграм бота."""

import os
import sys
import threading
import time
import logging
from typing import Any

# Built-in imports
from django.core.management.base import BaseCommand
from django.conf import settings

# Third-party imports

# Project imports


class Command(BaseCommand):
    """Команда Django для запуску телеграм бота."""

    help = "Run Telegram bot alongside Django server"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Ініціалізувати команду."""
        super().__init__(*args, **kwargs)
        self.bot_thread: threading.Thread | None = None
        self.bot_shutdown = threading.Event()

    def add_arguments(self, parser: Any) -> None:
        """Додати аргументи команди."""
        parser.add_argument(
            '--no-bot',
            action='store_true',
            help='Run Django without Telegram bot',
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Обробити виконання команди."""
        if options['no_bot']:
            self.stdout.write(
                self.style.WARNING(
                    'Running Django server without Telegram bot'
                )
            )
            # Run Django server normally
            os.system('python manage.py runserver')
            return

        self.stdout.write(
            self.style.SUCCESS(
                '🚀 Starting Django server with Telegram bot...'
            )
        )

        # Start bot in separate thread
        self.start_bot()

        try:
            # Run Django development server
            self.stdout.write(
                self.style.SUCCESS('🌐 Starting Django server...')
            )
            os.system('python manage.py runserver')

        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('\n🛑 Shutting down...')
            )
        finally:
            self.shutdown_bot()

    def start_bot(self) -> None:
        """Запустити телеграм бота в окремому потоці."""
        try:
            # Add telegram package to Python path
            telegram_path = os.path.join(settings.BASE_DIR, 'telegram')
            if telegram_path not in sys.path:
                sys.path.insert(0, telegram_path)

            # Import and start bot
            import importlib.util
            bot_spec = importlib.util.spec_from_file_location(
                "bot",
                os.path.join(telegram_path, "bot.py")
            )
            bot_main = None

            if bot_spec and bot_spec.loader:
                bot_module = importlib.util.module_from_spec(bot_spec)
                bot_spec.loader.exec_module(bot_module)
                bot_main = bot_module.main

            if not bot_main:
                raise ImportError("Could not import bot main function")

            def run_bot() -> None:
                """Запустити бота в потоці."""
                try:
                    import asyncio
                    if bot_main:
                        asyncio.run(bot_main())
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Bot error: {e}')
                    )

            self.bot_thread = threading.Thread(
                target=run_bot,
                daemon=True,
                name='TelegramBot'
            )

            self.bot_thread.start()

            self.stdout.write(
                self.style.SUCCESS('🤖 Telegram bot started successfully')
            )

        except ImportError as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to import bot: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to start bot: {e}')
            )

    def shutdown_bot(self) -> None:
        """Правильно зупинити телеграм бота."""
        if self.bot_thread and self.bot_thread.is_alive():
            self.stdout.write('🛑 Stopping Telegram bot...')
            self.bot_shutdown.set()

            # Wait for thread to finish
            self.bot_thread.join(timeout=10)

            if self.bot_thread.is_alive():
                self.stdout.write(
                    self.style.WARNING('⚠️ Bot thread did not stop gracefully')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✅ Telegram bot stopped')
                )