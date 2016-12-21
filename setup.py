#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='adhocracy4',
      version='0.0.0.dev1',
      description='Adhocracy 4 core library',
      license='AGPL-3+',
      author='Liquid Democracy e.V.',
      author_email='info@liqd.de',
      url='https://liqd.net/en/software/',
      packages=find_packages(exclude=['tests*']),
      install_requires = [
          'bleach',
          'Django >=1.8, <1.9',
          'djangorestframework >= 3.5, <4.0',
          'django-autoslug',
          'django-ckeditor',
          'python-magic',
          'rules',
      ],
     )
