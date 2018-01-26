#!/usr/bin/env python
from setuptools import setup, find_packages

requirements = None
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='SciELO WEB XML Validator',
    version='1.0',
    description='SciELO WEB XML Validator',
    author='Patricia Morimoto',
    author_email='excermori@gmail.com',
    packages=find_packages(),
    install_requires=requirements
)
