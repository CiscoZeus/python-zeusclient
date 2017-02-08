#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('test_requirements.txt') as f:
    test_requirements = f.read().splitlines()

setup(
    name='cisco-zeus',
    version='0.2.2.6',
    description="Python client for CiscoZeus.io. It allows a user to post/query logs and metrics using Zeus.",
    long_description=readme + '\n\n' + history,
    author="Marc Solanas Tarre",
    author_email='msolanas@cisco.com',
    url='https://github.com/CiscoZeus/python-zeusclient.git',
    packages=[
        'zeus',
        'zeus.interfaces',
    ],
    package_dir={
        'zeus': 'zeus',
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache License 2.0",
    zip_safe=False,
    keywords='zeus',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
