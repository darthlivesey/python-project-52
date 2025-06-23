#!/bin/bash
set -e

# Компиляция переводов (без sudo)
echo "### Compiling translations ###"
python src/manage.py compilemessages

# Применение миграций
echo "### Applying migrations ###"
python src/manage.py migrate

# Сбор статики
echo "### Collecting static files ###"
python src/manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"