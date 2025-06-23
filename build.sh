#!/bin/bash
set -e

# Используем UV для установки зависимостей из requirements.txt
echo "### Installing dependencies with UV ###"
uv pip install -r requirements.txt

# Добавляем путь к пакетам Python в PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/python/Python-${PYTHON_VERSION}/lib/python3.10/site-packages"

# Переходим в директорию src, где находится manage.py
cd src

# Компиляция переводов
echo "### Compiling translations ###"
python manage.py compilemessages

# Применение миграций
echo "### Applying migrations ###"
python manage.py migrate

# Сбор статики
echo "### Collecting static files ###"
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"