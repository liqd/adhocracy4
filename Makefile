VIRTUAL_ENV ?= .
SOURCE_DIRS = meinberlin apps

flake8:
	$(VIRTUAL_ENV)/bin/flake8 $(SOURCE_DIRS) --exclude migrations,settings.*

isort:
	$(VIRTUAL_ENV)/bin/isort -rc -c $(SOURCE_DIRS)

lint: flake8 isort
