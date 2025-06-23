#!/bin/bash
set -e

# Явно указать Python 3.10
export PATH="/opt/render/project/python/Python-3.10.18/bin:$PATH"

# Установка gettext для компиляции переводов
sudo apt-get update
sudo apt-get install -y gettext

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Компилируем переводы
python src/manage.py compilemessages

# Установить правильный PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/src"

# Применить миграции
python src/manage.py migrate

# Собрать статику
python src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"