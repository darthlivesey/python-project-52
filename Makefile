.PHONY: install build render-start migrate collectstatic test lint coverage prepare-hexlet start-server

install:
	uv pip install -r requirements.txt

build:
	./build.sh

render-start:
	gunicorn task_manager.config.wsgi:application

migrate:
	python manage.py migrate

run:
	python manage.py runserver

test:
	python manage.py test task_manager.tests --verbosity=2

lint:
	flake8 task_manager

coverage:
	coverage run --source='task_manager' manage.py test task_manager.tests
	coverage xml -i