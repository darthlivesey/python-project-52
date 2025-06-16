#!/bin/bash
set -e

# Явно указать Python 3.10
export PATH="/opt/render/project/python/Python-3.10.18/bin:$PATH"

# Установить uv локально
python -m pip install --user uv==0.7.13
export PATH="$HOME/.local/bin:$PATH"

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# Установить зависимости
uv pip install --python=python .

# Применить миграции
python manage.py migrate

# Собрать статику
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"