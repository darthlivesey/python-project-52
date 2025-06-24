#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
# Используем системный Python Render.com
PYTHON_BIN="/opt/render/project/python/Python-$PYTHON_VERSION/bin/python"

# Правильный путь к UV (из лога: "Using Python 3.10.18 environment at: /opt/render/project/python/Python-3.10.18")
UV_BIN="/opt/render/project/python/Python-$PYTHON_VERSION/bin/uv"

# Проверяем существование файлов перед выполнением
if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Python binary not found at $PYTHON_BIN"
    exit 1
fi

if [ ! -f "$UV_BIN" ]; then
    echo "Error: UV binary not found at $UV_BIN"
    exit 1
fi

# Устанавливаем зависимости
$UV_BIN pip install -r requirements.txt

echo "### Checking Django installation ###"
$PYTHON_BIN -c "import django; print(django.__file__)"

echo "### Debug: Current directory ###"
pwd
echo "### Debug: Directory contents ###"
ls -la
echo "### Debug: Python version ###"
$PYTHON_BIN --version
echo "### Debug: Installed packages ###"
$UV_BIN pip list
echo "### Debug: Python path ###"
$PYTHON_BIN -c "import sys; print(sys.path)"

echo "### Compiling translations ###"
$PYTHON_BIN src/manage.py compilemessages

echo "### Applying migrations ###"
$PYTHON_BIN src/manage.py migrate

echo "### Collecting static files ###"
$PYTHON_BIN src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"