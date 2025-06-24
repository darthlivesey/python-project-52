#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
# Используем системный Python Render.com
PYTHON_BIN="$(which python3.10)"
UV_BIN="$(which uv)"

# Устанавливаем зависимости
$UV_BIN pip install -r requirements.txt

echo "### Debug: Python path ###"
echo "Python binary: $PYTHON_BIN"
echo "UV binary: $UV_BIN"
$PYTHON_BIN --version

echo "### Debug: Installed packages ###"
$UV_BIN pip list

echo "### Compiling translations ###"
$PYTHON_BIN src/manage.py compilemessages

echo "### Applying migrations ###"
$PYTHON_BIN src/manage.py migrate

echo "### Collecting static files ###"
$PYTHON_BIN src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"