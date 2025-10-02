#!/usr/bin/env python
"""Скрипт для запуску Django з телеграм ботом."""

import os
import sys
import subprocess
import argparse
import platform

# Налаштувати UTF-8 кодування для Windows
if platform.system() == 'Windows':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Примусово налаштувати UTF-8 для stdout (без помилок линтера)
    try:
        # Використовуємо hasattr для перевірки доступності методу
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')  # type: ignore
    except (AttributeError, TypeError):
        # Fallback для старіших версій Python або помилок линтера
        pass

# Додати поточну директорію до Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


def get_venv_python_path() -> str:
    """ Отримати крос-платформний шлях до Python у віртуальному оточенні. """
    venv_path = os.path.join(current_dir, '.venv')

    # Визначити назву скриптової папки залежно від ОС
    if platform.system() == 'Windows':
        scripts_dir = 'Scripts'
        python_exec = 'python.exe'
    else:
        scripts_dir = 'bin'
        python_exec = 'python'

    python_path = os.path.join(venv_path, scripts_dir, python_exec)

    # Перевірити чи існує файл
    if os.path.exists(python_path):
        return python_path
    else:
        # Fallback до системного python
        return python_exec

def main() -> None:
    """Основна функція."""
    parser = argparse.ArgumentParser(description='Запуск Django з телеграм ботом')
    parser.add_argument('--no-bot', action='store_true', help='Запуск без бота')
    parser.add_argument('--test-path', action='store_true', help='Показати шлях до Python')
    parser.add_argument('django_args', nargs='*', help='Аргументи для Django команд')

    args = parser.parse_args()

    # Отримати правильний шлях до Python
    python_path = get_venv_python_path()

    # Показати шлях для тестування
    if args.test_path:
        print(f"🔍 Використовую Python: {python_path}")
        print(f"📂 ОС: {platform.system()}")
        return

    # Встановити змінні оточення
    env = os.environ.copy()
    env['PYTHONPATH'] = current_dir

    if args.no_bot:
        print("🌐 Запуск Django сервера без бота...")
        cmd = [python_path, 'manage.py'] + args.django_args
    else:
        print("🤖 Запуск Django сервера з телеграм ботом...")
        cmd = [python_path, 'manage.py', 'run_telegram_bot']

    # Запустити команду
    try:
        subprocess.run(cmd, env=env, cwd=current_dir)
    except KeyboardInterrupt:
        print("\n🛑 Зупинено користувачем")
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    main()