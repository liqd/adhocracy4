VIRTUAL_ENV ?= venv
NODE_BIN = node_modules/.bin

.PHONY: all
all: help

.PHONY: help
help:
	@echo mein.berlin development tools
	@echo
	@echo It will either use an exisiting virtualenv if it was entered
	@echo before or create a new one in the venv subdirectory.
	@echo
	@echo usage:
	@echo
	@echo "  make install         -- install dev setup"
	@echo "  make clean           -- delete node modules and venv"
	@echo "  make fixtures        -- install regions"
	@echo "  make server          -- start a dev server"
	@echo "  make watch           -- start a dev server and rebuild js and css files on changes"
	@echo "  make background      -- start a dev server, rebuild js and css files on changes, and start background processes"
	@echo "  make test            -- run all test cases with pytest"
	@echo "  make test-lastfailed -- run test that failed last"
	@echo "  make test-clean      -- test on new database"
	@echo "  make coverage        -- write coverage report to dir htmlcov"
	@echo "  make lint            -- lint all project files"
	@echo "  make lint-quick      -- lint all files staged in git"
	@echo "  make po              -- create new po files from the source"
	@echo "  make compilemessages -- create new mo files from the translated po files"
	@echo "  make release         -- build everything required for a release"
	@echo

.PHONY: install
install:
	npm install --no-save
	npm run build
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/python3 -m pip install --upgrade -r requirements/dev.txt
	$(VIRTUAL_ENV)/bin/python3 manage.py migrate

.PHONY: clean
clean:
	if [ -d node_modules ]; then rm -r node_modules; fi
	if [ -d venv ]; then rm -r venv; fi

.PHONY: fixtures
fixtures:
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/map-preset.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/site-dev.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/users-dev.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/orga-dev.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/project-dev.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/module-dev.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/phase-dev.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/admin-distr.json

.PHONY: server
server:
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8003

.PHONY: watch
watch:
	trap 'kill %1' KILL; \
	npm run watch & \
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8003

.PHONY: background
background:
	trap 'kill %1; kill %2' KILL; \
	npm run watch & \
	$(VIRTUAL_ENV)/bin/python3 manage.py process_tasks & \
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8003

.PHONY: test
test:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db

.PHONY: test-lastfailed
test-lastfailed:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db --last-failed

.PHONY: test-clean
test-clean:
	if [ -f test_db.sqlite3 ]; then rm test_db.sqlite3; fi
	$(VIRTUAL_ENV)/bin/py.test

.PHONY: coverage
coverage:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db --cov --cov-report=html

.PHONY: lint
lint:
	. $(VIRTUAL_ENV)/bin/activate && $(NODE_BIN)/polylint

.PHONY: lint-quick
lint-quick:
	. $(VIRTUAL_ENV)/bin/activate && $(NODE_BIN)/polylint -SF

.PHONY: po
po:
	$(VIRTUAL_ENV)/bin/python manage.py makemessages -d django
	$(VIRTUAL_ENV)/bin/python manage.py makemessages -d djangojs
	gsed -i 's%#: .*/adhocracy4%#: adhocracy4%' locale/*/LC_MESSAGES/django*.po
	msgen locale/en_GB/LC_MESSAGES/django.po -o locale/en_GB/LC_MESSAGES/django.po
	msgen locale/en_GB/LC_MESSAGES/djangojs.po -o locale/en_GB/LC_MESSAGES/djangojs.po

.PHONY: compilemessages
compilemessages:
	$(VIRTUAL_ENV)/bin/python manage.py compilemessages

.PHONY: release
release: export DJANGO_SETTINGS_MODULE ?= meinberlin.config.settings.build
release:
	npm install --silent
	npm run build:prod
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements.txt -q
	$(VIRTUAL_ENV)/bin/python3 manage.py compilemessages -v0
	$(VIRTUAL_ENV)/bin/python3 manage.py collectstatic --noinput -v0
