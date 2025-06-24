.PHONY: install build render-start migrate collectstatic test

install:
	uv pip install -r requirements.txt

build:
	./build.sh

render-start:
	cd src && gunicorn src.wsgi:application

migrate:
	python src/manage.py migrate

run:
	python src/manage.py runserver

test:
	python src/manage.py test task_manager

collectstatic:
	python src/manage.py collectstatic --noinput