#!/usr/bin/env python3

from setuptools import setup

setup(name='adhocracy4',
      version='0.0.0.dev1',
      description='Adhocracy 4 core library',
      license='AGPL-3+',
      author='Liquid Democracy e.V.',
      author_email='info@liqd.de',
      url='https://liqd.net/en/software/',
      packages=[
          'adhocracy4',
      ],
      zip_safe=False,  # allow to access using webpack
      install_requires = [
          'Django >=1.8, <1.9',
          'djangorestframework >= 3.5, <4.0',
      ],
     )
