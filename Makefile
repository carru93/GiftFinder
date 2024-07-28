INPUT_CSS = static/src/input.css
OUTPUT_CSS = static/src/output.css

install:
	pip install -r requirements.txt

test:
	python -m unittest discover -v

compile-css:
	npx tailwindcss -i $(INPUT_CSS) -o $(OUTPUT_CSS)

watch-css:
	npx tailwindcss -i $(INPUT_CSS) -o $(OUTPUT_CSS) --watch

clear-css:
	rm $(OUTPUT_CSS)

start-dev:
	python3 manage.py runserver & make watch-css

.PHONY: install test compile-css watch-css clear-css