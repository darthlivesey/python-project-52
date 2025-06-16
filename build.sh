#!/bin/bash
set -e  # Прерывать при ошибках

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# Установить UV
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Установить зависимости в виртуальное окружение
uv pip install --python=python .

# Применить миграции
python manage.py migrate

# Собрать статику
python manage.py collectstatic --noinput --clear