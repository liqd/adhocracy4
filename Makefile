VIRTUAL_ENV ?= .env
NODE_BIN = node_modules/.bin

all: help

.PHONY: help
help:
	@echo mein.berlin development tools
	@echo
	@echo It will either use an exisiting virtualenv if it was entered
	@echo before or create a new one in the .env subdirectory.
	@echo
	@echo usage:
	@echo
	@echo "  make install         -- install dev setup"
	@echo "  make build           -- build js and css and create new po and mo files"
	@echo "  make lint            -- lint all project files"
	@echo "  make server          -- start a dev server"
	@echo "  make watch           -- start a dev server and rebuild js and css files on changes"
	@echo "  make test            -- run all test cases with pytest"
	@echo "  make makemessages    -- create new po files from the source"
	@echo "  make compilemessages -- create new mo files from the translated po files"
	@echo

.PHONY: install
install:
	npm install --no-save
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements/dev.txt
	$(VIRTUAL_ENV)/bin/python3 manage.py migrate

.PHONY: webpack
webpack:
	$(NODE_BIN)/webpack --config webpack.dev.js

.PHONY: webpack-prod
webpack-prod:
	$(NODE_BIN)/webpack --config webpack.prod.js

.PHONY: makemessages
makemessages:
	$(VIRTUAL_ENV)/bin/python manage.py makemessages -d django
	$(VIRTUAL_ENV)/bin/python manage.py makemessages -d djangojs
	sed -i 's%#: .*/adhocracy4%#: adhocracy4%' locale/*/LC_MESSAGES/django*.po
	msgen locale/en_GB/LC_MESSAGES/django.po -o locale/en_GB/LC_MESSAGES/django.po
	msgen locale/en_GB/LC_MESSAGES/djangojs.po -o locale/en_GB/LC_MESSAGES/djangojs.po

.PHONY: makemessages
compilemessages:
	$(VIRTUAL_ENV)/bin/python manage.py compilemessages

.PHONY: build
build: webpack compilemessages

.PHONY: server
server:
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8000

.PHONY: watch
watch:
	$(NODE_BIN)/webpack --config webpack.dev.js --watch & \
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8000

.PHONY: lint
lint:
	. $(VIRTUAL_ENV)/bin/activate && $(NODE_BIN)/polylint

.PHONY: lint-quick
lint-quick:
	. $(VIRTUAL_ENV)/bin/activate && $(NODE_BIN)/polylint -SF

.PHONY: test
test:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db

.PHONY: test-lastfailed
test-lastfailed:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db --last-failed

.PHONY: test-clean
test-clean:
	if [ -f test_db.sqlite3 ]; then rm test_db.sqlite3; fi
