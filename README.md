# Participation platform mein.berlin

mein.berlin is a participation platform for the city of Berlin, Germany. It is
based on [adhocracy 4](https://github.com/liqd/adhocracy4).

![Build Status](https://github.com/liqd/a4-meinberlin/actions/workflows/django.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/liqd/a4-meinberlin/badge.svg?branch=main)](https://coveralls.io/github/liqd/a4-meinberlin?branch=main)

## Requirements

*   nodejs (+ npm)
*   python 3.x (+ venv + pip)
*   libmagic
*   libjpeg
*   libpq (only if postgres should be used)
*   gdal
*   sqlite3 [with JSON1 enabled](https://code.djangoproject.com/wiki/JSON1Extension)

## Installation (for development and testing only!)

    git clone https://github.com/liqd/a4-meinberlin.git
    cd a4-meinberlin
    make install
    make fixtures
    make watch

### Use postgresql database for testing:
run the following command once:
```
make create-postgres
```
to start the testserver with postgresql, run:
```
export DATABASE=postgresql
make start-postgres
make watch
```
