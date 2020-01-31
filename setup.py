#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def readlines(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).readlines()


version = read('VERSION')

requirements = readlines('requirements.txt')

test_requirements = [
    'tox',
    'coverage',
    'fakeredis==0.8.2'
]

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: Public Domain
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(
    name='robotframework-redislibrary',
    version=version,
    description="robotframework-redislibrary is a Robot Framework test library for manipulating in-memory data which store in Redis",
    author="Traitanit Huangsri",
    author_email='traitanit.hua@gmail.com',
    url='https://github.com/nottyo/robotframework-redislibrary.git',
    packages=[
        'RedisLibrary'
    ],
    package_dir={'robotframework-redislibrary':
                 'RedisLibrary'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='robotframework redislibrary redis',
    classifiers=CLASSIFIERS.splitlines(),
    test_suite='tests',
    tests_require=test_requirements
)
