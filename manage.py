#!/usr/bin/env python
"""Django management command wrapper."""
import os
import sys

if __name__ == "__main__":
    # Добавляем директорию src в путь Python
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Устанавливаем переменную окружения для Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
    
    # Импортируем и запускаем стандартный manage.py из src
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)