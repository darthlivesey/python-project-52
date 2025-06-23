.PHONY: install build render-start migrate collectstatic

install:
	uv pip install -r requirements.txt

build:
	./build.sh

render-start:
	.venv/bin/gunicorn src.wsgi

migrate:
	python src/manage.py makemigrations
	python src/manage.py migrate

run:
	python src/manage.py runserver

test:
	python src/manage.py test task_manager

collectstatic:
	python src/manage.py collectstatic --noinput