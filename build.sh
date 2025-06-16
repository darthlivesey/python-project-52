#!/bin/bash
set -e

# Явно указать Python 3.10
export PATH="/opt/render/project/python/Python-3.10.18/bin:$PATH"

# Создать виртуальное окружение
python -m venv .venv

# Активировать окружение
source .venv/bin/activate

# Установить зависимости с помощью pip
pip install --upgrade pip
pip install -r requirements.txt

# Установить пути
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/src"

# Применить миграции (используя Python из виртуального окружения)
.venv/bin/python manage.py migrate

# Собрать статику
.venv/bin/python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"