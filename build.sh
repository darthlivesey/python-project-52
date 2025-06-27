#!/bin/bash
set -o errexit

echo "### Creating virtual environment ###"
python3.10 -m venv .venv
source .venv/bin/activate

echo "### Installing dependencies with pip ###"
pip install -r requirements.txt
pip install --upgrade pip

echo "### Debug: Python path ###"
python --version
pip list

echo "### Applying migrations ###"
cd src
export DJANGO_SETTINGS_MODULE=src.settings

python manage.py makemigrations --noinput || echo "No new migrations needed"
python manage.py migrate

echo "### Compiling translations ###"
mkdir -p ../../locale/ru/LC_MESSAGES
touch ../../locale/ru/LC_MESSAGES/django.po

python manage.py compilemessages

echo "### Verifying translations ###"
ls -l ../../locale/ru/LC_MESSAGES
cd ..

echo "### Collecting static files ###"
python src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"