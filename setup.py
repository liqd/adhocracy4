#!/usr/bin/env python3

from setuptools import find_packages
from setuptools import setup

setup(name='adhocracy4',
      version='0.0.0.dev1',
      description='Adhocracy 4 core library',
      license='AGPL-3+',
      author='Liquid Democracy e.V.',
      author_email='info@liqd.de',
      url='https://liqd.net/en/software/',
      packages=find_packages(exclude=['tests*']),
      include_package_data=True,
      install_requires=[
          'bleach',
          'Django >=1.8',
          'django-allauth',
          'django-autoslug',
          'django-background-tasks',
          'django-ckeditor',
          'django-filter',
          'django-widget-tweaks',
          'djangorestframework >= 3.5, <4.0',
          'easy-thumbnails',
          'jsonfield',
          'python-dateutil',
          'python-magic',
          'rules',
      ],
     )
