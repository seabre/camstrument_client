#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='camstrument_client',
    version='0.1.0',
    description="Camstrument Client",
    long_description=readme + '\n\n' + history,
    author="Sean Brewer",
    author_email='seabre986@gmail.com',
    url='https://github.com/seabre/camstrument_client',
    packages=[
        'camstrument_client',
    ],
    package_dir={'camstrument_client':
                 'camstrument_client'},
    entry_points={
        'console_scripts': ['camstrument_client = camstrument_client.__main__:main'],
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='camstrument_client',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
