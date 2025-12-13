# сборка проекта
install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput
	
build:
	./build.sh

# запуск приложения на render.com
render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check
