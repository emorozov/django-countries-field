#!/usr/bin/env python
import sys
from argparse import ArgumentParser

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'country_field_test',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        },

        INSTALLED_APPS=[
            'countries_field',
            'countries_field.tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        EXTRA_COUNTRIES=[None, None, ('XC', u'Crimea')]
    )


def runtests(*test_args, **kwargs):
    if not test_args:
        test_args = ['countries_field']

    django.setup()
    test_runner = DiscoverRunner(**kwargs)

    failures = test_runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--verbosity', dest='verbosity', action='store',
                      default=1, type=int)
    parser.add_arguments(DiscoverRunner.options)
    (options, args) = parser.parse_args()

    runtests(*args, **options.__dict__)
