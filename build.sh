#!/bin/bash
set -x  # Режим отладки

# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "### Python version: $(python --version)"
echo "### UV version: $(uv --version)"

# Установка зависимостей
uv pip install --python=python .

# Проверка установки Django
echo "### Installed Django:"
python -c "import django; print(django.__version__)"

# Применение миграций
python manage.py migrate

# Сборка статики
python manage.py collectstatic --noinput --clear

echo "### Build completed successfully ###"