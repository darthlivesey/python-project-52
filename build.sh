#!/bin/bash
set -o errexit

echo "### Проверка и создание структуры проекта ###"
echo "Содержимое корневой папки:"
ls -la

echo "### Создание необходимых симлинков в code/ ###"
mkdir -p code
ln -sfn ../src code/src || true
ln -sfn ../task_manager code/task_manager || true
ln -sfn ../src/manage.py code/manage.py || true

echo "### Проверка созданных симлинков ###"
echo "Содержимое code/:"
ls -la code
echo "Проверка src:"
ls -l code/src
echo "Проверка task_manager:"
ls -l code/task_manager
echo "Проверка manage.py:"
ls -l code/manage.py

echo "### Копирование venv ###"
cp -r .venv code/ || echo "Копирование venv пропущено"
ls -la code/.venv || echo "Venv не скопирован"

echo "### Установка зависимостей ###"
pip install -r requirements.txt
pip install --upgrade pip

echo "### Проверка установки Django ###"
./.venv/bin/python -c "import django; print('Django version:', django.__version__)" || echo "Django not found!"

echo "### Применение миграций ###"
cd src
export DJANGO_SETTINGS_MODULE=src.settings

python manage.py makemigrations --noinput || echo "No new migrations needed"
python manage.py migrate

echo "### Компиляция переводов ###"
python manage.py compilemessages

echo "### Проверка переводов ###"
if [ -f "../locale/ru/LC_MESSAGES/django.mo" ]; then
    echo "Russian translation found"
else
    echo "WARNING: Russian translation not found!"
    echo "Содержимое locale:"
    ls -R ../locale
fi

echo "### Сборка статических файлов ###"
python manage.py collectstatic --noinput --clear

echo "### Сборка завершена успешно ###"