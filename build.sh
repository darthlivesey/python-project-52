#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
# Используем системный Python Render.com
PYTHON_BIN="/opt/render/project/python/Python-$PYTHON_VERSION/bin/python"
UV_BIN="/opt/render/project/python/Python-$PYTHON_VERSION/bin/uv"

# Устанавливаем зависимости в системное окружение Render.com
$UV_BIN pip install -r requirements.txt

echo "### Checking Django installation ###"
$PYTHON_BIN -c "import django; print(django.__file__)"

echo "### Compiling translations ###"
$PYTHON_BIN src/manage.py compilemessages

echo "### Applying migrations ###"
$PYTHON_BIN src/manage.py migrate

echo "### Collecting static files ###"
$PYTHON_BIN src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"