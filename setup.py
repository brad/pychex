#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from setuptools import setup


req = [line for line in open('requirements/base.txt').read().split("\n")]
req_test = [line for line in open('requirements/test.txt').read().split("\n")]

pcinit = open('pychex/__init__.py').read()
author = re.search("__author__ = '([^']+)'", pcinit).group(1)
author_email = re.search("__author_email__ = '([^']+)'", pcinit).group(1)
version = re.search("__version__ = '([^']+)'", pcinit).group(1)

setup(
    name='pychex',
    version=version,
    description='Paychex library',
    long_description=open('README.rst').read(),
    author=author,
    author_email=author_email,
    url='https://github.com/brad/pychex',
    packages=['pychex'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=['setuptools'] + req,
    license='Apache 2.0',
    tests_require=req_test,
    entry_points={
        'console_scripts': ['pychex=pychex.cli:main'],
    },
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)
