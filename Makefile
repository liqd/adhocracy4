VIRTUAL_ENV ?= .env
NODE_BIN = node_modules/.bin
SOURCE_DIRS = meinberlin apps
SCSS_FILES := $(shell find 'meinberlin/assets/scss' -name '*.scss')
PO_FILES := $(shell find . -name '*.po')

install:
	npm install
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements/dev.txt
	$(VIRTUAL_ENV)/bin/python3 manage.py migrate

meinberlin/static/style.css: meinberlin/assets/scss/style.scss $(SCSS_FILES)
	$(NODE_BIN)/node-sass $< $@

makemessages:
	$(VIRTUAL_ENV)/bin/python manage.py makemessages

compilemessages: $(PO_FILES)
	$(VIRTUAL_ENV)/bin/python manage.py compilemessages

build: meinberlin/static/style.css compilemessages

server:
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8000

flake8:
	$(VIRTUAL_ENV)/bin/flake8 $(SOURCE_DIRS) --exclude migrations,settings.*

isort:
	$(VIRTUAL_ENV)/bin/isort -sl -rc -c $(SOURCE_DIRS)

stylelint:
	$(NODE_BIN)/stylelint --syntax scss 'meinberlin/assets/scss/**/*.scss'

lint: flake8 isort stylelint
