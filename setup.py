# -*- coding: utf-8 -*-

from setuptools import setup
from os.path import abspath, dirname, join

path = abspath(dirname(__file__))

classifiers = (
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'License :: OSI Approved :: MIT License',
)

required = (
    'matplotlib',
    'numpy',
    'pandas',
    'nltk',
    'husl'
)

kw = {
    'name': 'climatic',
    'version': '0.1.0',
    'description': 'A small toolbox of wind data plotting tools',
    'long_description': open(join(path, 'README.md')).read(),
    'author': 'Rob Story',
    'author_email': 'wrobstory@gmail.com',
    'license': 'MIT License',
    'url': 'https://github.com/wrobstory/climatic',
    'keywords': 'wind data plotting',
    'classifiers': classifiers,
    'modules': ['climatic'],
    'install_requires': required,
    'zip_safe': True,
}

setup(**kw)
