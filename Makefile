all: help

VIRTUAL_ENV ?= .
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
	$(VIRTUAL_ENV)/bin/python3 setup.py development

lint:
	$(VIRTUAL_ENV)/bin/flake8 $(SOURCE_DIRS) --exclude migrations,settings*

test:
	$(VIRTUAL_ENV)/bin/pytest
