VIRTUAL_ENV ?= .env
NODE_BIN = node_modules/.bin
SCSS_FILES := $(shell find 'meinberlin/assets/scss' -name '*.scss')
PO_FILES := $(shell find . -name '*.po')

install:
	npm install
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements/dev.txt
	$(VIRTUAL_ENV)/bin/python3 manage.py migrate

meinberlin/static/style.css: meinberlin/assets/scss/style.scss $(SCSS_FILES)
	$(NODE_BIN)/node-sass $< $@

scss: meinberlin/static/style.css

makemessages:
	$(VIRTUAL_ENV)/bin/python manage.py makemessages

compilemessages: $(PO_FILES)
	$(VIRTUAL_ENV)/bin/python manage.py compilemessages

build: scss compilemessages

server:
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8000
