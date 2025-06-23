#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
uv pip install -r requirements.txt

# Основная директория проекта
PROJECT_DIR="/opt/render/project/src"

# Добавляем пути в PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PROJECT_DIR}/src:/opt/render/project/python/Python-${PYTHON_VERSION}/lib/python3.10/site-packages"

# Устанавливаем модуль настроек
export DJANGO_SETTINGS_MODULE="settings"

# Переходим в директорию с настройками
cd ${PROJECT_DIR}/src

echo "### Debug: Current directory ###"
pwd
echo "### Debug: Directory contents ###"
ls -la
echo "### Debug: PYTHONPATH ###"
echo $PYTHONPATH
echo "### Debug: Django settings module ###"
echo $DJANGO_SETTINGS_MODULE

echo "### Compiling translations ###"
python manage.py compilemessages

echo "### Applying migrations ###"
python manage.py migrate

echo "### Collecting static files ###"
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"