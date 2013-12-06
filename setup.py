#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

required = [
    'requests>=2.0.1'
]

setup(
    name='muddle',
    version='0.1.0',
    description='Moodle 2.0 WebService API Wrapper.',
    long_description=open('README.rst').read() + '\n\n' +
    open('HISTORY.rst').read(),
    author='Kit Randel',
    author_email='kit@nocturne.net.nz',
    url='https://github.com/squidsoup/muddle.py',
    packages=['muddle'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=required,
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
    ),
)
