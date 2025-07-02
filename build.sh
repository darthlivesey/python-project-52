#!/bin/bash
set -o errexit

echo "### Reorganizing project structure ###"
mkdir -p task_manager
mv config/* task_manager/
mv locale task_manager/
mv templates task_manager/
mv tests task_manager/
mv task_manager/*.py task_manager/tasks/

echo "### Installing dependencies ###"
pip install -r requirements.txt
pip install --upgrade pip

echo "### Applying migrations ###"
python manage.py makemigrations --noinput || echo "No new migrations needed"
python manage.py migrate

echo "### Compiling translations ###"
python manage.py compilemessages

echo "### Verifying translations ###"
if [ -f "task_manager/locale/ru/LC_MESSAGES/django.mo" ]; then
    echo "Russian translation found"
else
    echo "WARNING: Russian translation not found!"
    echo "Contents of task_manager/locale directory:"
    find task_manager/locale -type f
fi

echo "### Collecting static files ###"
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"