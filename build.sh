#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
uv venv
uv pip install -r requirements.txt

echo "### Checking Django installation ###"
.venv/bin/python -c "import django; print(django.__file__)"

echo "### Compiling translations ###"
.venv/bin/python src/manage.py compilemessages

echo "### Applying migrations ###"
.venv/bin/python src/manage.py migrate

echo "### Collecting static files ###"
.venv/bin/python src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"