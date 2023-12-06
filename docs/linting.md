# Linting

We use a set of linters to check our code for errors and to provide commands for
auto formatting.

## Linters

### Python and Django

#### Black

We use black to format all our python code. It is run as part of the commit hook
and auto formats all staged code. It can also be invoked manually as part of the
`lint-python-files` command:

```
make lint-python-files <path>
# example for linting all python files for mb
make lint-python-files meinberlin
```

For details on black see https://github.com/psf/black

#### Djlint

We use djlint to check all django templates for errors. It is run as part of the
commit hook and checks all staged code. It can also be invoked manually via the
`lint-html-files` command:

```
make lint-html-files <path>
# example for linting all template files for mb
make lint-html-files meinberlin
```

We also provide a command for auto formatting django templates:

```
make lint-html-fix <path>
# example for fixing the base.html template
make lint-html-fix meinberlin/templates/base.html
```

**Note** There are currently a lot of open bug reports about the auto formatting
breaking stuff, so use this with caution.

We disabled the following rules as we currently don't make use of them:

- H030 Consider adding a meta description.
- H031 Consider adding meta keywords.

For details on djlint see https://github.com/Riverside-Healthcare/djLint/

#### Isort

We use isort to check all our python code for broken or unused imports . It is
run as part of the commit hook and checks and auto resolves issues (if possible)
on all staged code. It can also be invoked manually as part of the
`lint-python-files` command if you want to lint a specific file or folder or as
part of the `lint` command to lint all files:

```
# lint all python files
make lint
# lint  specific python file or folder
make lint-python-files <path>
# example for linting all python files for mb
make lint-python-files meinberlin
```

For details on isort see https://github.com/PyCQA/isort

#### Flake8

We use flake8 to check and enforce the codestyle for all our python code. It is
run as part of the commit hook and checks all staged code. It can also be
invoked manually as part of the`lint-python-files` command if you want to lint
a specific file or folder or as part of the `lint` command to lint all files:

```
# lint all python files
make lint
# lint specific python file or folder
make lint-python-files <path>
# example for linting all python files for mb
make lint-python-files meinberlin
```

For details on black see https://github.com/PyCQA/flake8

### JS / CSS

#### Eslint

We use eslint to check and enforce the codestyle for all our javascript code.
It is run as part of the commit hook and checks all staged code. It can also be
invoked manually via `npm run lint` to check the code and via `npm run lint-fix`
to attempt to automatically fix issues in all js files.

For configuration specifics see the eslint config file `.eslintrc`.

For details on eslint see https://github.com/eslint/eslint

#### Stylelint

We use stylelint to check and enforce the codestyle for all our (s)css files.
It is run as part of the commit hook and checks all staged code. It can also be
invoked manually via `npm run lint` to check the code.

For configuration specifics see the stylelint config file `.stylelintrc.json`.

For details on eslint see https://github.com/stylelint/stylelint
