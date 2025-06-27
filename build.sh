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
export DJANGO_SETTINGS_MODULE=src.settings

python src/manage.py makemigrations --noinput || echo "No new migrations needed"

python src/manage.py migrate

echo "### Compiling translations ###"
python src/manage.py compilemessages

echo "### Collecting static files ###"
python src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"