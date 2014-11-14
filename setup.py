#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from setuptools import setup

required = [line for line in open('requirements/base.txt').read().split("\n")]
required_test = [line for line in open('requirements/test.txt').read().split("\n") if not line.startswith("-r")]

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
    install_requires=["setuptools"] + required,
    license='Apache 2.0',
    tests_require=required + required_test,
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ),
)
