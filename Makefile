# сборка проекта
install:
	uv sync

build:
	./build.sh

# запуск приложения на render.com
render-start:
	gunicorn task_manager.wsgi

