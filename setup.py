#!/usr/bin/env python
# Based on: https://github.com/kennethreitz/setup.py/blob/master/setup.py
"""
Setup tools
Use setuptools to install package dependencies. Instead of a requirements file you
can install directly from this file.
`pip install .`
You can install dev dependencies by targeting the appropriate key in extras_require
```
pip install .[dev] # install requires and test requires
pip install '.[dev]' # install for MAC OS / zsh

```
See: https://packaging.python.org/tutorials/installing-packages/#installing-setuptools-extras
"""
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'intellistop'
DESCRIPTION = 'Library to determine a intelligent stop-loss for technical analysis of funds.'
URL = 'https://github.mmm.com/nga-27/intellistop'
EMAIL = 'namell91@gmail.com'
AUTHOR = 'Nick Amell'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '1.0.0'

# What packages are required for this module to be executed?
REQUIRES = [
    "numpy==1.24.1",
    "pandas==1.5.2",
    "scipy==1.9.3",
    "yfinance==0.2.3",
]

REQUIRES_APP = [
    "matplotlib==3.5.1"
]

REQUIRES_DEV = [
    "pylint==2.15.0"
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=[
            "*.tests",
            "*.tests.*"
            "tests.*",
            "tests",
            "test"
        ]
    ),
    install_requires=REQUIRES,
    extras_require={
        'dev': REQUIRES_DEV,
        'app': REQUIRES_APP
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
