#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
# Создаем виртуальное окружение и устанавливаем зависимости
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Переходим в директорию src
cd src

echo "### Compiling translations ###"
python manage.py compilemessages

echo "### Applying migrations ###"
python manage.py migrate

echo "### Collecting static files ###"
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"