#!/usr/bin/env python
# Copyright (c) 2016 Russell Gunther
# For license information, see the LICENSE file
# I'd like to thank Bryan Worrell for directing me in creating a proper python
# package and for inspiring me to list this on pypi. Also for generally being
# an awesome mentor
import os
import setuptools


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(BASE_DIR, "circuit_breaker", 'version.py')
README_FILE = os.path.join(BASE_DIR, "README.md")


def normalize(version):
    return version.split()[-1].strip("\"'")


def get_version():
    with open(VERSION_FILE) as f:
        version = next(line for line in f if line.startswith("__version__"))
        return normalize(version)

setuptools.setup(
    name="circuitbreaker",
    description="Circuit breaker pattern implemenation to protect systems from external failures",
    author="Russell Gunther",
    url="https://github.com/rgunther30/circuitbreaker",
    version=get_version(),
    packages=setuptools.find_packages(),
    include_package_data=True
)
