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
	@echo "### STARTING SERVER WITH PYTHON 3.10 ###"
	cd code && \
	python3.10 --version && \
	python3.10 -m venv .venv && \
	. .venv/bin/activate && \
	pip list && \
	python -c "import django; print('Django version:', django.__version__)" && \
	python manage.py runserver 0.0.0.0:3000