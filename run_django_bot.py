#!/usr/bin/env python
"""Скрипт для запуску Django з телеграм ботом."""

import os
import sys
import subprocess
import argparse

# Додати поточну директорію до Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    """Основна функція."""
    parser = argparse.ArgumentParser(description='Запуск Django з телеграм ботом')
    parser.add_argument('--no-bot', action='store_true', help='Запуск без бота')
    parser.add_argument('django_args', nargs='*', help='Аргументи для Django команд')

    args = parser.parse_args()

    # Встановити змінні оточення
    env = os.environ.copy()
    env['PYTHONPATH'] = current_dir

    if args.no_bot:
        print("🌐 Запуск Django сервера без бота...")
        cmd = ['.venv/bin/python', 'manage.py'] + args.django_args
    else:
        print("🤖 Запуск Django сервера з телеграм ботом...")
        cmd = ['.venv/bin/python', 'manage.py', 'run_telegram_bot']

    # Запустити команду
    try:
        subprocess.run(cmd, env=env, cwd=current_dir)
    except KeyboardInterrupt:
        print("\n🛑 Зупинено користувачем")
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    main()