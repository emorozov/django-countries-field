# coding: utf-8
import gettext
import pycountry
from django.conf import settings
from django.forms import MultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from .countries_list import ALL_COUNTRIES, EXTRA_COUNTRIES


class CountriesFormField(MultipleChoiceField):
    """ Поле формы для поддержки поля модели CountriesField. """

    def __init__(self, choices=None, *args, **kwargs):
        """ Задает в choices список стран по стандарту iso3166.
        :param choices: Переопределяет набор использыемых стран.
        :param args:
        :param kwargs:
        :return:
        """
        if choices is None:
            choices = self.generate_countries_choices()
        kwargs['widget'] = FilteredSelectMultiple(kwargs.get('label'), False)
        super(CountriesFormField, self).__init__(choices=choices, *args,
                                                 **kwargs)

    def generate_countries_choices(self):
        """ Генерирует choices для стран по iso3166. """
        choices = [(c.alpha2, c.name) for c in pycountry.countries
                                      if c.alpha2 in ALL_COUNTRIES]
        choices += [c for c in EXTRA_COUNTRIES if c]
        if settings.USE_I18N:
            try:
                lang = settings.LANGUAGE_CODE[0:2]
                locale = gettext.translation('iso3166', pycountry.LOCALES_DIR,
                                         languages=[lang])
                choices = ((k, locale.ugettext(v)) for k, v in choices)
            except IOError:
                pass

        return sorted(choices, key=lambda x: x[1])
