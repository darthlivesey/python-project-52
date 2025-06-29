#!/bin/bash
set -o errexit

echo "### COPYING VENV TO CODE ###"
cp -r .venv code/
ls -la code/.venv

echo "### Installing dependencies with pip ###"
pip install -r requirements.txt
pip install --upgrade pip

echo "### Verifying Django installation ###"
./.venv/bin/python -c "import django; print('Django version:', django.__version__)" || echo "Django not found!"

echo "### Applying migrations ###"
cd src
export DJANGO_SETTINGS_MODULE=src.settings

python manage.py makemigrations --noinput || echo "No new migrations needed"
python manage.py migrate

echo "### Compiling translations ###"
python manage.py compilemessages

echo "### Verifying translations ###"
if [ -f "../locale/ru/LC_MESSAGES/django.mo" ]; then
    echo "Russian translation found"
else
    echo "WARNING: Russian translation not found!"
    echo "Contents of locale directory:"
    ls -R ../locale
fi

echo "### Collecting static files ###"
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"