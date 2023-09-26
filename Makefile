VIRTUAL_ENV ?= venv
NODE_BIN = node_modules/.bin
SOURCE_DIRS = meinberlin tests
ARGUMENTS=$(filter-out $(firstword $(MAKECMDGOALS)), $(MAKECMDGOALS))

# for mac os gsed is needed (brew install gnu-sed and brew install gsed)
SED = sed
ifneq (, $(shell command -v gsed;))
	SED = gsed
endif

# checks the OS uname respones (mac will respond with Darwin)
OS := $(shell uname)

	START_NOW := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

ifeq ($(OS),Darwin)
	END_NOW = $(shell date -u -v+30d +"%Y-%m-%dT%H:%M:%SZ")
	START_2 = $(shell date -u -v+30d +"%Y-%m-%dT%H:%M:%SZ")
	END_2 = $(shell date -u -v+30d +"%Y-%m-%dT%H:%M:%SZ")
	START_3 = $(shell date -u -v+30d +"%Y-%m-%dT%H:%M:%SZ")
	END_3 = $(shell date -u -v+30d +"%Y-%m-%dT%H:%M:%SZ")
else
	END_NOW = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+30 days")
	START_2 = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+31 days")
	END_2 = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+61 days")
	START_3 = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+62 days")
	END_3 = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+92 days")
endif

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
	@echo "  make install					-- install dev setup"
	@echo "  make clean						-- delete node modules and venv"
	@echo "  make fixtures					-- install regions"
	@echo "  make server					-- start a dev server"
	@echo "  make watch						-- start a dev server and rebuild js and css files on changes"
	@echo "  make background				-- start background processes"
	@echo "  make test						-- run all test cases"
	@echo "  make pytest					-- run all test cases with pytest"
	@echo "  make pytest-lastfailed			-- run test that failed last"
	@echo "  make pytest-clean				-- test on new database"
	@echo "  make jstest					-- run js tests with coverage"
	@echo "  make jstest-nocov				-- run js tests without coverage"
	@echo "  make jstest-debug				-- run changed tests only, no coverage"
	@echo "  make jstest-updateSnapshots	-- update jest snapshots"
	@echo "  make coverage					-- write coverage report to dir htmlcov"
	@echo "  make lint						-- lint all project files"
	@echo "  make lint-quick				-- lint all files staged in git"
	@echo "  make lint-fix					-- fix linting for all js files staged in git"
	@echo "  make lint-python-files			-- lint all python files staged in git"
	@echo "  make po						-- create new po files from the source"
	@echo "  make mo						-- create new mo files from the translated po files"
	@echo "  make release					-- build everything required for a release"
	@echo "  make start-postgres			-- start the local postgres cluster"
	@echo "  make stop-postgres				-- stops the local postgres cluster"
	@echo "  make create-postgres			-- create the local postgres cluster (only works on ubuntu 20.04)"
	@echo "  make local-a4					-- patch to use local a4 (needs to have path ../adhocracy4)"
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
	if [ -f package-lock.json ]; then rm package-lock.json; fi
	if [ -d node_modules ]; then rm -rf node_modules; fi
	if [ -d venv ]; then rm -rf venv; fi

.PHONY: fixtures
fixtures:
	# set start date of active phase to today
	$(SED) -i "s/2022-12-31T23:00:00Z/$(START_NOW)/g" meinberlin/fixtures/phases.json
	$(SED) -i "s/2023-01-31T22:59:00Z/$(END_NOW)/g" meinberlin/fixtures/phases.json
	# set start date of upcoming phase to today + 31
	$(SED) -i "s/2023-01-31T23:00:00Z/$(START_2)/g" meinberlin/fixtures/phases.json
	$(SED) -i "s/2023-02-28T22:59:00Z/$(END_2)/g" meinberlin/fixtures/phases.json
	# set start date of last phase to today + 62
	$(SED) -i "s/2023-02-28T23:00:00Z/$(START_3)/g" meinberlin/fixtures/phases.json
	$(SED) -i "s/2023-03-31T21:59:00Z/$(END_3)/g" meinberlin/fixtures/phases.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/site-dev.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/users.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/accounts.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/administrative_districts.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/map-preset.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/organisations.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/projects.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/modules.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/phases.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/maps.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/polls.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/live_questions.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/categories.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/documents.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/labels.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/maptopicprop.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/moderationtasks.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/topicprio.json
	$(VIRTUAL_ENV)/bin/python3 manage.py loaddata meinberlin/fixtures/votes.json
	git restore meinberlin/fixtures/phases.json

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
	$(VIRTUAL_ENV)/bin/python3 manage.py process_tasks

.PHONY: test
test:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db
	npm run testNoCov

.PHONY: pytest
pytest:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db

.PHONY: pytest-lastfailed
pytest-lastfailed:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db --last-failed

.PHONY: pytest-clean
pytest-clean:
	if [ -f test_db.sqlite3 ]; then rm test_db.sqlite3; fi
	$(VIRTUAL_ENV)/bin/py.test

.PHONY: jstest
jstest:
	npm run test

.PHONY: jstest-nocov
jstest-nocov:
	npm run testNoCov

.PHONY: jstest-debug
jstest-debug:
	npm run testDebug

.PHONY: jstest-updateSnapshots
jstest-updateSnapshots:
	npm run updateSnapshots

.PHONY: coverage
coverage:
	$(VIRTUAL_ENV)/bin/py.test --reuse-db --cov --cov-report=html

.PHONY: lint
lint:
	EXIT_STATUS=0; \
	$(VIRTUAL_ENV)/bin/isort --diff -c $(SOURCE_DIRS) ||  EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/flake8 $(SOURCE_DIRS) --exclude migrations,settings ||  EXIT_STATUS=$$?; \
	npm run lint ||  EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/python manage.py makemigrations --dry-run --check --noinput || EXIT_STATUS=$$?; \
	exit $${EXIT_STATUS}

.PHONY: lint-quick
lint-quick:
	EXIT_STATUS=0; \
	npm run lint-staged ||  EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/python manage.py makemigrations --dry-run --check --noinput || EXIT_STATUS=$$?; \
	exit $${EXIT_STATUS}

.PHONY: lint-fix
lint-fix:
	EXIT_STATUS=0; \
	npm run lint-fix ||  EXIT_STATUS=$$?; \
	exit $${EXIT_STATUS}

.PHONY: lint-python-files
lint-python-files:
	EXIT_STATUS=0; \
	$(VIRTUAL_ENV)/bin/black $(ARGUMENTS) || EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/isort --diff -c $(ARGUMENTS) --filter-files || EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/flake8 $(ARGUMENTS) || EXIT_STATUS=$$?; \
	exit $${EXIT_STATUS}

.PHONY: po
po:
	$(VIRTUAL_ENV)/bin/python manage.py makemessages --all -d django --extension html,email,py --ignore '$(CURDIR)/node_modules/adhocracy4/adhocracy4/*'
	$(VIRTUAL_ENV)/bin/python manage.py makemessages --all -d djangojs --ignore '$(VIRTUAL_ENV)/*' --ignore '$(CURDIR)/node_modules/dsgvo-video-embed/dist/*'
	$(foreach file, $(wildcard locale/*/LC_MESSAGES/django*.po), \
		$(SED) -i 's%#: .*/adhocracy4%#: adhocracy4%' $(file);)
	$(foreach file, $(wildcard locale/*/LC_MESSAGES/django*.po), \
		$(SED) -i 's%#: .*/dsgvo-video-embed/js%#: dsgvo-video-embed/js%' $(file);)
	msgen locale/en_GB/LC_MESSAGES/django.po -o locale/en_GB/LC_MESSAGES/django.po
	msgen locale/en_GB/LC_MESSAGES/djangojs.po -o locale/en_GB/LC_MESSAGES/djangojs.po

.PHONY: mo
mo:
	$(VIRTUAL_ENV)/bin/python manage.py compilemessages

.PHONY: release
release: export DJANGO_SETTINGS_MODULE ?= meinberlin.config.settings.build
release:
	npm install --silent
	npm run build:prod
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements.txt -q
	$(VIRTUAL_ENV)/bin/python3 manage.py compilemessages -v0
	$(VIRTUAL_ENV)/bin/python3 manage.py collectstatic --noinput -v0

.PHONY: start-postgres
start-postgres:
	sudo -u postgres PGDATA=pgsql PGPORT=5555 /usr/lib/postgresql/12/bin/pg_ctl start

.PHONY: stop-postgres
stop-postgres:
	sudo -u postgres PGDATA=pgsql PGPORT=5555 /usr/lib/postgresql/12/bin/pg_ctl stop

.PHONY: create-postgres
create-postgres:
	if [ -d "pgsql" ]; then \
		echo "postgresql has already been initialized"; \
	else \
		sudo install -d -m 774 -o postgres -g $(USER) pgsql; \
		sudo -u postgres /usr/lib/postgresql/12/bin/initdb pgsql; \
		sudo -u postgres PGDATA=pgsql PGPORT=5555 /usr/lib/postgresql/12/bin/pg_ctl start; \
		sudo -u postgres PGDATA=pgsql PGPORT=5555 /usr/lib/postgresql/12/bin/createuser -s django; \
		sudo -u postgres PGDATA=pgsql PGPORT=5555 /usr/lib/postgresql/12/bin/createdb -O django django; \
		sudo -u postgres PGDATA=pgsql PGPORT=5555 /usr/lib/postgresql/12/bin/pg_ctl stop; \
	fi

.PHONY: local-a4
local-a4:
	if [ -d "../adhocracy4" ]; then \
		$(VIRTUAL_ENV)/bin/python -m pip install --upgrade ../adhocracy4; \
		$(VIRTUAL_ENV)/bin/python manage.py migrate; \
		npm link ../adhocracy4; \
	fi
