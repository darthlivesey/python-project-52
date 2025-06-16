#!/bin/bash
set -e

# Явно указать Python 3.10
export PATH="/opt/render/project/python/Python-3.10.18/bin:$PATH"

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Установить правильный PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/src"

# Применить миграции
python src/manage.py migrate

# Собрать статику
python src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"