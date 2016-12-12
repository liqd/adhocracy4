VIRTUAL_ENV ?= .
SOURCE_DIRS = meinberlin apps

install:
	npm install
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements/dev.txt
	$(VIRTUAL_ENV)/bin/python3 manage.py migrate

flake8:
	$(VIRTUAL_ENV)/bin/flake8 $(SOURCE_DIRS) --exclude migrations,settings.*

isort:
	$(VIRTUAL_ENV)/bin/isort -rc -c $(SOURCE_DIRS)

lint: flake8 isort
