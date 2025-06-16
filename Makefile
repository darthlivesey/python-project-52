.PHONY: install build render-start migrate collectstatic

install:
	uv pip install -r requirements.txt

build:
	./build.sh

render-start:
	.venv/bin/gunicorn src.wsgi

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput