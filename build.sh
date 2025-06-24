#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
# Создаем виртуальное окружение
uv venv
# Устанавливаем зависимости
uv pip install -r requirements.txt

# Определяем абсолютный путь к Python в виртуальном окружении
PYTHON_BIN="$(pwd)/.venv/bin/python"

echo "### Compiling translations ###"
$PYTHON_BIN src/manage.py compilemessages

echo "### Applying migrations ###"
$PYTHON_BIN src/manage.py migrate

echo "### Collecting static files ###"
$PYTHON_BIN src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"