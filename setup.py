#!/usr/bin/env python
import os
from setuptools import find_packages, setup
import warnings


def parse_requirements(filename):
    """ Parse a requirements file ignoring comments and -r inclusions of other files """
    reqs = []
    with open(filename, 'r') as f:
        for line in f:
            hash_idx = line.find('#')
            if hash_idx >= 0:
                line = line[:hash_idx]
            line = line.strip()
            if line:
                reqs.append(line)
    return reqs


with open('README.md', 'rb') as f:
    readme = str(f.read().strip())


setup(
    name="tulsa",
    version="0.1",
    url="https://github.com/dssg/tulsa",
    author="Awesome people",
    author_email="dssg@uchicago.edu",
    license="Proprietary",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.in'),
    tests_require=parse_requirements('requirements.testing.in'),
    description="Code related to the tulsa schools project",
    entry_points="""
    [console_scripts]
    hypervisor=tulsa.learn.cli_hypervisor:main
    """,
    long_description="\n" + readme
)
