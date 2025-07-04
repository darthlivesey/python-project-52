.PHONY: install build render-start migrate collectstatic test lint coverage prepare-hexlet start-server

install:
	uv pip install -e .

migrate:
	uv run python3 manage.py migrate

run:
	uv run manage.py runserver

test:
	python manage.py test task_manager.tests --verbosity=2

coverage:
	coverage run --source='.' manage.py test task_manager.tests
	coverage report
	coverage xml

makemessages:
	uv run django-admin makemessages --ignore="static" --ignore=".env"  -l ru

compilemessages:
	uv run django-admin compilemessages

collectstatic:
	uv run python3 manage.py collectstatic --no-input

build:
	./build.sh

render-start:
	gunicorn task_manager.config.wsgi:application

lint:
	uv run ruff check task_manager

format-app:
	uv run ruff check --fix task_manager

check:
	ruff check .
	python manage.py test task_manager.tests --verbosity=2