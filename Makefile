all: help

VIRTUAL_ENV ?= venv
SOURCE_DIRS = adhocracy4 tests
NODE_BIN = node_modules/.bin
ARGUMENTS=$(filter-out $(firstword $(MAKECMDGOALS)), $(MAKECMDGOALS))

help:
	@echo Adhocracy4 development tools
	@echo
	@echo It will either use a exisiting virtualenv if it was entered
	@echo before or create a new one in the same directory.
	@echo
	@echo usage:
	@echo 	make clean   	 			-- delete node modules and venv
	@echo   make lint	 				-- lint javascript and python
	@echo   make lint-quick     		-- lint all files staged in git
	@echo   make lint-python-files	 	-- lint python
	@echo   make lint-fix      			-- fix linting for js files staged in git
	@echo   make test     				-- run all tests front and backend
	@echo   make jest    				-- run js tests with coverage
	@echo   make jest-nocov    	 		-- run js tests without coverage
	@echo   make jest-debug    			-- run changed tests only, no coverage
	@echo   make jest-updateSnapshots   -- update jest snapshots


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
	EXIT_STATUS=0; \
	$(VIRTUAL_ENV)/bin/isort --diff -c $(SOURCE_DIRS) ||  EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/flake8 $(SOURCE_DIRS) --exclude migrations,settings ||  EXIT_STATUS=$$?; \
	npm run lint ||  EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/python manage.py makemigrations --dry-run --check --noinput || EXIT_STATUS=$$?; \
	exit $${EXIT_STATUS}

.PHONY: lint-quick
lint-quick:
	EXIT_STATUS=0; \
	npm run lint-staged || EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/python manage.py makemigrations --dry-run --check --noinput || EXIT_STATUS=$$?; \
	exit $${EXIT_STATUS}

.PHONY: lint-python-files
lint-python-files:
	EXIT_STATUS=0; \
	$(VIRTUAL_ENV)/bin/black $(ARGUMENTS) || EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/isort --diff -c $(ARGUMENTS) --filter-files || EXIT_STATUS=$$?; \
	$(VIRTUAL_ENV)/bin/flake8 $(ARGUMENTS) || EXIT_STATUS=$$?; \
	exit $${EXIT_STATUS}

.PHONY: lint-fix
lint-fix:
	EXIT_STATUS=0; \
	npm run lint-fix ||  EXIT_STATUS=$$?; \
	exit $${EXIT_STATUS}

.PHONY: test
test:
	$(VIRTUAL_ENV)/bin/pytest --reuse-db
	npm run testNoCov

.PHONY: jest
jest:
	npm run test

.PHONY: jest-nocov
jest-nocov:
	npm run testNoCov

.PHONY: jest-debug
jest-debug:
	npm run testDebug

.PHONY: jest-updateSnapshots
jest-updateSnapshots:
	npm run updateSnapshots
