#!/bin/bash
set -e

echo "### Installing dependencies with UV ###"
uv pip install -r requirements.txt

# Создаем временный manage.py в корне проекта
MAIN_DIR="/opt/render/project/src"
echo "import sys" > ${MAIN_DIR}/manage.py
echo "from src.manage import main" >> ${MAIN_DIR}/manage.py
echo "if __name__ == '__main__':" >> ${MAIN_DIR}/manage.py
echo "    main()" >> ${MAIN_DIR}/manage.py

# Переходим в корень проекта
cd ${MAIN_DIR}

echo "### Compiling translations ###"
python manage.py compilemessages

echo "### Applying migrations ###"
python manage.py migrate

echo "### Collecting static files ###"
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"