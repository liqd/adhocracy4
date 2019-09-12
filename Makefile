all: help

VIRTUAL_ENV ?= venv
SOURCE_DIRS = adhocracy4 tests

help:
	@echo Adhocracy4 development tools
	@echo
	@echo It will either use a exisiting virtualenv if it was entered
	@echo before or create a new one in the same directory.
	@echo
	@echo usage:
	@echo
	@echo   make lint	  -- lint javascript and python

.PHONY: install
install:
	npm install
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/pip install -r requirements/dev.txt

.PHONY: clean
clean:
	if [ -f package-lock.json ]; then rm package-lock.json; fi
	if [ -d node_modules ]; then rm -rf node_modules; fi
	if [ -d venv ]; then rm -rf venv; fi

.PHONY: lint
lint:
	. $(VIRTUAL_ENV)/bin/activate && node_modules/.bin/polylint

.PHONY: lint-quick
lint-quick:
	. $(VIRTUAL_ENV)/bin/activate && node_modules/.bin/polylint -SF

.PHONY: test
test:
	$(VIRTUAL_ENV)/bin/pytest --reuse-db
