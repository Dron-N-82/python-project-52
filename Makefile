build:
	./build.sh

# запуск приложения на render.com
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

