#!/bin/bash
set -e

# Явно указать Python 3.10
export PATH="/opt/render/project/python/Python-3.10.18/bin:$PATH"

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# Установить uv
pip install uv==0.7.13

# Установить зависимости проекта
uv pip install -r requirements.txt

# Активировать окружение для последующих команд
source .venv/bin/activate

# Применить миграции
python manage.py migrate

# Собрать статику
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"