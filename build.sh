#!/bin/bash
set -o errexit

echo "### Reorganizing project structure ###"
mkdir -p config
mv src/settings.py config/base.py
touch config/__init__.py
mv src/urls.py config/
mv src/wsgi.py config/
[ -f src/asgi.py ] && mv src/asgi.py config/

echo "### Moving templates and static files ###"
mkdir -p templates
mv task_manager/templates/* templates/ || echo "No templates to move"

echo "### Installing dependencies ###"
pip install -r requirements.txt
pip install --upgrade pip

echo "### Applying migrations ###"
python manage.py makemigrations --noinput || echo "No new migrations needed"
python manage.py migrate

echo "### Compiling translations ###"
python manage.py compilemessages

echo "### Verifying translations ###"
if [ -f "locale/ru/LC_MESSAGES/django.mo" ]; then
    echo "Russian translation found"
else
    echo "WARNING: Russian translation not found!"
    echo "Contents of locale directory:"
    find locale -type f
fi

echo "### Collecting static files ###"
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"