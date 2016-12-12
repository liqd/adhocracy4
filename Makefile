VIRTUAL_ENV ?= .
NODE_BIN = node_modules/.bin
SOURCE_DIRS = meinberlin apps
SCSS_FILES := $(shell find 'meinberlin/assets/scss' -name '*.scss')

install:
	npm install
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements/dev.txt
	$(VIRTUAL_ENV)/bin/python3 manage.py migrate

meinberlin/static/style.css: meinberlin/assets/scss/style.scss $(SCSS_FILES)
	$(NODE_BIN)/node-sass $< $@

flake8:
	$(VIRTUAL_ENV)/bin/flake8 $(SOURCE_DIRS) --exclude migrations,settings.*

isort:
	$(VIRTUAL_ENV)/bin/isort -rc -c $(SOURCE_DIRS)

stylelint:
	$(NODE_BIN)/stylelint --syntax scss 'meinberlin/assets/scss/**/*.scss'

lint: flake8 isort stylelint
