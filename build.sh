#!/bin/bash
set -e

echo "### Creating virtual environment ###"
python3.10 -m venv .venv
source .venv/bin/activate

echo "### Installing dependencies with pip ###"
pip install -r requirements.txt

echo "### Debug: Python path ###"
python --version
pip list

echo "### Applying migrations ###"
python src/manage.py migrate

echo "### Compiling translations ###"
cd src
python manage.py compilemessages
cd ..

echo "### Collecting static files ###"
python src/manage.py collectstatic --noinput --clear

echo "### Verifying translations ###"
ls -l src/locale/ru/LC_MESSAGES

echo "### Build completed successfully ###"