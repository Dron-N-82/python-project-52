# сборка проекта
install:
	uv sync

dev:
	uv run manage.py runserver 0.0.0.0:8081

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate
	
build:
	./build.sh

# запуск приложения на render.com
render-start:
	gunicorn task_manager.wsgi

test:
	uv run pytest --ds=task_manager.settings --reuse-db -v -l

lint:
	uv run ruff check .
