#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
uv pip install -r requirements.txt

# Добавляем путь к пакетам Python в PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/python/Python-${PYTHON_VERSION}/lib/python3.10/site-packages"

# Устанавливаем PYTHONPATH так, чтобы он включал корень проекта
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Явно указываем модуль настроек (без префикса пакета)
export DJANGO_SETTINGS_MODULE="settings"

# Переходим в директорию src, где находится manage.py и settings.py
cd src

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