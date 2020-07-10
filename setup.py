#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import abspath, dirname, join

# Get version
version_file = join(dirname(abspath(__file__)), 'RedisLibrary', 'version.py')
with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

requirements = [
    'robotframework>=3.0',
    'redis>=2.10.5'
]

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

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='robotframework-redislibrary',
    version=VERSION,
    description="robotframework-redislibrary is a Robot Framework test library for manipulating in-memory data which store in Redis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Traitanit Huangsri",
    author_email='traitanit.hua@gmail.com',
    url='https://github.com/robotframework-thailand/robotframework-redislibrary.git',
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
