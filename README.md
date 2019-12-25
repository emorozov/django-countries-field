django-countries-field
=====

[![Build Status](https://travis-ci.org/rutube/django-countries-field.svg)](https://travis-ci.org/rutube/django-countries-field)

Django model field which can store multiple selected countries.

Requirements
=====
* Django>=1.9.0,<2.0.0
* pycountry>=1.20

Installation
=====

Install it with pip (or easy_install):

```pip install django-countries-field```


Usage
=====

```
# coding: utf-8
from django.db import models
from countries_field.fields import CountriesField


class TestCountriesModel(models.Model):
    countries = CountriesField()
```

More example, see: `countries_field/tests/tests.py`
