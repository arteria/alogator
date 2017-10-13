#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import alogator as app

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = app.__version__


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="alogator",
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, app, logging, event, action, aggregator, alogator',
    author='arteria GmbH',
    author_email='admin@arteria.ch',
    url="https://github.com/arteria/alogator",
    packages=[
        'alogator',
    ],
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    scripts=['alogator/alogator_cli'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
