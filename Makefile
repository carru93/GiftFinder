INPUT_CSS = static/src/input.css
OUTPUT_CSS = static/src/output.css

install:
	pip install -r requirements.txt;\
	pre-commit install

test:
	python3 manage.py test

compile-css:
	npx tailwindcss -i $(INPUT_CSS) -o $(OUTPUT_CSS)

watch-css:
	npx tailwindcss -i $(INPUT_CSS) -o $(OUTPUT_CSS) --watch

clear-css:
	rm $(OUTPUT_CSS)

start-dev:
	trap 'kill 0' SIGINT; python3 manage.py runserver & make watch-css

polish:
	pre-commit run --all-files

init-db:
	python3 manage.py migrate;\
	python3 manage.py loaddata giftcategories;\
	python3 manage.py loaddata hobbies;

seed:
	@if [ -e db.sqlite3 ]; then rm db.sqlite3; fi;\
	make init-db;\
	python3 manage.py random-seeder;
	python manage.py setup_moderators_group;

.PHONY: install test compile-css watch-css clear-css polish start-dev init-db seed
