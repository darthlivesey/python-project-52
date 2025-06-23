#!/bin/bash
set -e

# Определяем путь к интерпретатору Python
PYTHON_BIN="/opt/render/project/python/Python-$PYTHON_VERSION/bin/python"

# Используем UV для установки зависимостей из requirements.txt
echo "### Installing dependencies with UV ###"
uv pip install -r requirements.txt

# Компиляция переводов
echo "### Compiling translations ###"
$PYTHON_BIN src/manage.py compilemessages

# Применение миграций
echo "### Applying migrations ###"
$PYTHON_BIN src/manage.py migrate

# Сбор статики
echo "### Collecting static files ###"
$PYTHON_BIN src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"