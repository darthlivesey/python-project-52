#!/bin/bash
set -e

# Используем UV для установки зависимостей из requirements.txt
echo "### Installing dependencies with UV ###"
uv pip install -r requirements.txt

# Компиляция переводов
echo "### Compiling translations ###"
python src/manage.py compilemessages

# Применение миграций
echo "### Applying migrations ###"
python src/manage.py migrate

# Сбор статики
echo "### Collecting static files ###"
python src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"