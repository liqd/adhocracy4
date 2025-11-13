Adhocracy4
==========

A library for building online participation software.
It is maintained and developed by Liquid Democracy e.V. and
heavily relies on the Django web framework.

Examples of using adhocracy4 are [a+](https://github.com/liqd/adhocracy-plus),
[meinBerlin](https://github.com/liqd/a4-meinberlin) and
[Civic Europe](https://github.com/liqd/a4-civic-europe). The first two being
online participation platforms implementing different processes like idea
collections or debates, and the latter using adhocracy4 as the basis for a
transparent idea challenge.

To try it out yourself, best start with [a+][https://github.com/liqd/adhocracy-plus/blob/main/docs/installation_prod.md].

![Build Status](https://github.com/liqd/adhocracy4/actions/workflows/django.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/liqd/adhocracy4/badge.svg?branch=main)](https://coveralls.io/github/liqd/adhocracy4?branch=main)

### Local Development

## Adhocracy4 Installation

    git clone https://github.com/liqd/adhocracy4.git
    cd adhocracy4
    make install

Global setup: `make install` uses pipx to install uv system-wide
Project isolation: It then uses uv to create a local `.venv` and installs dependencies into it.

## Use Make
    make test
    make help

## Development
To add a new Library use uv 
```
uv add module
```
this automaticly updates pyproject.toml and uv.lock

## Virtual Enviroment
if you want to do something inside the venv manually use
```
uv run python manage.py ...
```
(which invokes .venev/bin/python manage.py ... )





### Tested With

[<img src="http://www.browserstack.com/images/layout/browserstack-logo-600x315.png" alt="Browser Stack Logo" width="300">](https://www.browserstack.com/)
