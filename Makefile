.PHONY: install build render-start migrate collectstatic test lint coverage prepare-hexlet start-server

install:
	uv pip install -r requirements.txt

build:
	./build.sh

render-start:
	gunicorn config.wsgi:application

migrate:
	python manage.py migrate

run:
	python manage.py runserver

test:
	python manage.py test tests --verbosity=2

lint:
	flake8 config task_manager

coverage:
	coverage run --source='.' manage.py test task_manager
	coverage xml -i