#!/usr/bin/env python

from setuptools import setup, find_packages
from countries_field import __version__


setup(
    name='django-countries-field',
    version=__version__,
    author='RUTUBE',
    author_email='devel@rutube.ru',
    url='https://github.com/rutube/django-countries-field',
    description='Django countries bitfield.',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'Django>=1.7,<1.10',
        'pycountry==1.20',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
