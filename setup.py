#!/usr/bin/env python3

from setuptools import find_packages
from setuptools import setup

__version__ = '0.0.0.dev1'

setup(name='a4-meinberlin-libs',
      version=__version__,
      description='meinBerlin adhocracy 4 library apps',
      license='AGPL-3+',
      author='Liquid Democracy e.V.',
      author_email='info@liqd.de',
      url='https://mein.berlin.de/',
      packages=find_packages(exclude=['tests*', 'meinberlin.config*']),
      include_package_data=True,
      install_requires=[
          'adhocracy4',
          'bcrypt',
          'django-capture-tag',
          'html5lib',
          'wagtail',
          'XlsxWriter',
          'zeep',
      ])
