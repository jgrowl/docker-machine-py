#!/usr/bin/env python
import os
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

requirements = [
    'docker-py==1.6.0',
    'enum34'
]

exec(open('docker/machine/version.py').read())

with open('./test-requirements.txt') as test_reqs_txt:
    test_requirements = [line for line in test_reqs_txt]

version = None
exec(open('docker/machine/version.py').read())

setup(
    name="docker-machine-py",
    version=version,
    description="Python wrapper for Docker Machine.",
    url='https://github.com/jgrowl/docker-machine-py/',
    packages=[
        'docker.machine', 'docker.machine.cli',
    ],
    install_requires=requirements,
    tests_require=test_requirements,
    zip_safe=False,
    test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
)
