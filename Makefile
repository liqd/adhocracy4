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

install:
	npm install
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/pip install -r requirements/dev.txt

lint:
	. $(VIRTUAL_ENV)/bin/activate && node_modules/.bin/polylint

lint-quick:
	. $(VIRTUAL_ENV)/bin/activate && node_modules/.bin/polylint -SF

test:
	$(VIRTUAL_ENV)/bin/pytest
