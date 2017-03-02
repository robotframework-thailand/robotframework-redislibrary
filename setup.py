#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from RedisLibrary.version import VERSION

requirements = [
    'tox',
    'coverage',
    'robotframework>=3.0',
    'redis==2.10.5'
]

test_requirements = [
    # TODO: put package test requirements here
]

long_description = """RedisLibrary is a Robot Framework keywords for manipulating in-memory data which store in Redis.

    == Redis ==
    Redis is an open-source software project (sponsored by Redis Labs) that implements data structure servers. It is networked, in-memory, and stores keys with optional durability.

    `resources.robot`
    | *** Settings *** |
    | Library          |  RedisLibrary  |

    """

setup(
    name='robotframework-redislibrary',
    version=VERSION,
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
    keywords='robotframework-redislibrary',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: QA',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    long_description=long_description,
    tests_require=test_requirements
)
