.PHONY: install build render-start migrate collectstatic

install:
	uv pip install -r requirements.txt

.PHONY: build
build:
	./build.sh
	
render-start:
	.venv/bin/gunicorn src.wsgi

migrate:
	python src/manage.py makemigrations
	python src/manage.py migrate

.PHONY: run
run:
	python src/manage.py runserver

.PHONY: test
test:
	python src/manage.py test task_manager

collectstatic:
	python src/manage.py collectstatic --noinput