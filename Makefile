.PHONY: install build render-start migrate collectstatic test lint coverage

install:
	uv pip install -r requirements.txt

build:
	./build.sh

render-start:
	gunicorn src.wsgi:application --pythonpath src

migrate:
	python src/manage.py migrate

run:
	python src/manage.py runserver

test:
	python src/manage.py test task_manager --verbosity=2

lint:
	flake8 src task_manager

coverage:
	coverage run --source='.' src/manage.py test task_manager
	coverage xml -i