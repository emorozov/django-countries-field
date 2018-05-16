# coding: utf-8
from __future__ import absolute_import
import unittest
from django.conf import settings
from django.forms import model_to_dict
from django.test import TestCase

from countries_field.fields import (CountriesValue, countries_contains,
                                    countries_contains_exact, countries_exact,
                                    countries_isnull,
                                    countries_to_bin, bin_to_countries)
from countries_field.forms import CountriesFormField

from .models import TestCountriesModel


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """ Подключает тестовые модели и синкает базу с ними """
        cls._installed_apps = settings.INSTALLED_APPS
        settings.INSTALLED_APPS.append("countries_field.tests")
        from django.core.management import call_command
        call_command('migrate', verbosity=0)

    @classmethod
    def tearDownClass(cls):
        """ Отключаем тестовое приложение. """
        settings.INSTALLED_APPS = cls._installed_apps


class CountriesFieldTests(BaseTestCase):
    def setUp(self):
        self.initial_countries = ["ru", "UA", "Au", "XC"]
        self.testee = TestCountriesModel.objects.create(
            countries=self.initial_countries)

    def testCreate(self):
        """ Позволяет задать список стран при инициализации. """
        check = TestCountriesModel.objects.get(pk=self.testee.pk)
        self.assertEqual(self.initial_countries, check.countries)

    def testSetNewValue(self):
        """ Позволяет задать новый список стран. """
        new_value = ["gb", "us", "au"]
        for expected in (new_value, CountriesValue(countries=new_value)):
            self.testee.countries = new_value
            self.testee.save()
            check = TestCountriesModel.objects.get(pk=self.testee.pk)
            self.assertEqual(expected, check.countries)

    def setEmptyList(self):
        """ Пустой список сбрасывает все установлденные страны. """
        new_value = ()
        self.testee.countries = new_value
        self.testee.save()
        check = TestCountriesModel.objects.get(pk=self.testee.pk)
        self.assertEqual(new_value, check.countries)

    def testAddCountries(self):
        """ Позволяет дополнить список стран. """
        countries = ["Gb", "US"]
        for added in (countries, CountriesValue(countries=countries)):
            self.testee.countries |= added
            self.testee.save()
            check = TestCountriesModel.objects.get(pk=self.testee.pk)
            self.assertEqual(list(self.initial_countries) + countries,
                             check.countries)

    def testRemoveCountries(self):
        """ Позволяет исключить список стран. """
        expected = self.initial_countries[:]
        delete_country = expected.pop()
        expected.reverse()
        for deleted in ((delete_country,),
                        CountriesValue(countries=(delete_country,))):
            self.testee.countries -= deleted
            self.testee.save()
            check = TestCountriesModel.objects.get(pk=self.testee.pk)
            self.assertEqual(expected, check.countries)

    def testContains(self):
        """ Позволяет проверить вхождение списка стран. """
        self.assertTrue("ru" in self.testee.countries)
        self.assertFalse("Invalid" in self.testee.countries)

    def testEqual(self):
        """ Сравнение работает парвильно для одинаковых списков стран. """
        for expected in (self.initial_countries,
                         CountriesValue(countries=self.initial_countries)):
            self.assertEquals(expected, self.testee.countries)

    def testNotEqual(self):
        """ Сравнение работает правильно для разных списков стран. """
        countries = self.initial_countries[:-1]
        for expected in (countries, CountriesValue(countries=countries)):
            self.assertNotEquals(expected, self.testee.countries)

    @unittest.expectedFailure
    def testLookup(self):
        check = TestCountriesModel.objects.get(countries=["ru"])

    def testBoolean(self):
        """ Приведение к булевому значению: если ни одной страны не задано,
        то False, иначе - True. """
        self.assertTrue(self.testee.countries)

        self.testee.countries = []
        self.testee.save()
        check = TestCountriesModel.objects.get(pk=self.testee.pk)
        self.assertFalse(check.countries)

    def testModelToDict(self):
        try:
            model_to_dict(self.testee)
        except Exception as e:
            self.fail(e)

    def testInheritance(self):
        """ Проверяет, что поле со странами можно унаследовать"""
        from .models import TestCountriesChildModel
        child_model = TestCountriesChildModel.objects.create(countries=self.initial_countries)
        self.assertEqual(self.initial_countries, child_model.countries)


class FiltersTestCase(BaseTestCase):
    def setUp(self):
        self.country1 = TestCountriesModel.objects.create(countries=[])
        self.country2 = TestCountriesModel.objects.create(countries=['ru', 'us', 'fr'])
        self.country3 = TestCountriesModel.objects.create(countries=['ru', 'ua'])
        self.country4 = TestCountriesModel.objects.create(countries=['ru'])

    def testIsNull(self):
        countries = TestCountriesModel.objects.filter(countries_isnull())

        self.assertEqual(countries.count(), 1)
        self.assertIn(self.country1, countries)

    def testContains(self):
        countries = TestCountriesModel.objects.filter(countries_contains(['us', 'ua']))

        self.assertEqual(countries.count(), 2)
        self.assertIn(self.country2, countries)
        self.assertIn(self.country3, countries)

    def testExact(self):
        countries = TestCountriesModel.objects.filter(countries_exact(['RU']))

        self.assertEqual(countries.count(), 1)
        self.assertIn(self.country4, countries)

    def testContainsExact(self):
        countries = TestCountriesModel.objects.filter(countries_contains_exact(['ru', 'fr']))

        self.assertEqual(countries.count(), 1)
        self.assertIn(self.country2, countries)


class CrimeaTestCase(BaseTestCase):

    def test_countries_to_bin(self):
        bins = countries_to_bin(["XC"])
        self.assertEqual(bins, [0, 0, 0, 2**62])

    def test_bin_to_countries(self):
        countries = bin_to_countries([0, 0, 0, 2**62])
        self.assertEqual(countries, ["XC"])

    def test_contains_exact(self):
        self.country = TestCountriesModel.objects.create(countries=['xc'])
        countries = TestCountriesModel.objects.filter(countries_exact(['XC']))

        self.assertEqual(countries.count(), 1)
        self.assertIn(self.country, countries)


class FormFieldChoicesTestCase(BaseTestCase):

    def test_generate_countries_choices(self):
        field = CountriesFormField()
        choices = field.generate_countries_choices()
        self.assertIn((u'RU', u'Russian Federation'), choices)
        self.assertIn((u'XC', u'Crimea'), choices)
