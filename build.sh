#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
export PATH="$HOME/.local/bin:$PATH"

# Явная установка gunicorn
/opt/render/.local/bin/uv pip install gunicorn

# Установка зависимостей
/opt/render/.local/bin/uv pip install -e .

python manage.py migrate

python manage.py collectstatic --noinput
