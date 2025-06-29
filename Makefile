.PHONY: install build render-start migrate collectstatic test lint coverage prepare-hexlet start-server

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

prepare-hexlet:
	mkdir -p code
	cp -r src code/
	cp -r task_manager code/
	cp manage.py code/
	cp requirements.txt code/

start-server:
	cd code && \
	if [ -d .venv ]; then \
		. .venv/bin/activate && \
		python manage.py runserver 0.0.0.0:3000; \
	else \
		echo "Creating virtual environment..." && \
		python3.10 -m venv .venv && \
		. .venv/bin/activate && \
		pip install -r requirements.txt && \
		python manage.py runserver 0.0.0.0:3000; \
	fi