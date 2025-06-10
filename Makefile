.PHONY: install build render-start migrate collectstatic

install:
	uv pip install -r requirements.txt

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput