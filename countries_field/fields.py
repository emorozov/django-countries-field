# coding: utf-8
from django.db import models
from django.db.models.fields.subclassing import Creator

from .bitfield.models import BitField, MAX_FLAG_COUNT
from .forms import CountriesFormField
from .countries_list import ALPHA2_INDEX, ALL_COUNTRIES
# Допустимые биты для хранения стран.
VALID_BINARY_MASK = (1 << MAX_FLAG_COUNT) - 1

ALPHA2_MAP = {c: p for p, c in enumerate(ALL_COUNTRIES) if c is not None}


def get_bit_field_name(i, name="countries", prefix=""):
    return "{}_{}_b{}".format(prefix, name, i)


def countries_to_bin(countries):
    binaries = [0, 0, 0, 0]
    for c in countries:
        c_num = ALPHA2_MAP[c.upper()]
        byte_num = int(c_num / MAX_FLAG_COUNT)
        bit_num = c_num % MAX_FLAG_COUNT
        try:
            binaries[byte_num] |= 1 << bit_num
        except Exception as e:
            import pdb; pdb.set_trace()
    return binaries


def bin_to_countries(binaries):
    """ Превращает все установленные биты в первых 4-х элементах списка в
    список стран.
    :param binaries: Список из 4 элементов шириной MAX_FLAG_COUNT каждый
    :return: Список 2-х буквенных кодов стран

    """
    countries = []
    for byte_num in range(4):
        byte = binaries[byte_num] & VALID_BINARY_MASK
        byte_shift = byte_num * MAX_FLAG_COUNT
        bit_num = 0
        while byte:
            if byte & 0b1:
                countries.append(ALL_COUNTRIES[byte_shift + bit_num])
            byte >>= 1
            bit_num += 1
    return countries


def countries_contains(countries, prefix=""):
    """ Возвращает Q-объект отфильтровывающий строки, содержащие в себе
    значения любой из указанных стран

    :param countries: список стран для поиска
    :param prefix: префикс к названию поля
    :return: models.Q
    """
    contains_q = models.Q()
    for c in countries:
        contains_q |= countries_contains_exact([c], prefix=prefix)
    return contains_q


def countries_contains_exact(countries, prefix=""):
    """ Возвращает Q-объект отфильтровывающий строки, содержащие в себе
    значения всех указанных стран

    :param countries: список стран для поиска
    :param prefix: префикс к названию поля
    :return: models.Q
    """
    countries = countries_to_bin(countries)
    contains_q = models.Q(**{get_bit_field_name(i, prefix=prefix):
                             models.F(get_bit_field_name(i, prefix=prefix)).bitor(b)
                             for i, b in enumerate(countries)})
    return contains_q


def countries_exact(countries, prefix=""):
    """ Возвращает Q-объект отфильтровывающий строки, точно совпадающие с
    указанным списком стран

    :param countries: список стран для поиска
    :param prefix: префикс к названию поля
    :return: models.Q
    """
    countries = countries_to_bin(countries)
    return models.Q(**{get_bit_field_name(i, prefix=prefix): b
                       for i, b in enumerate(countries)})


def countries_isnull(prefix=""):
    """ Возвращает Q-объект отфильтровывающий строки с пустым списком стран
    :param prefix: префикс к названию поля
    """
    return countries_exact([], prefix=prefix)


class CountriesValue(object):
    """ Представление набора заданых стран.
    """
    def __init__(self, binaries=None, countries=None):
        self.binaries = [int(b) & VALID_BINARY_MASK
                         for b in (binaries or [0, 0, 0, 0])]
        if isinstance(countries, (list, tuple)):
            countries = countries_to_bin(countries)
            for i in range(4):
                self.binaries[i] |= countries[i]

    def __iter__(self):
        for c in bin_to_countries(self.binaries):
            yield c

    def __len__(self):
        return len(bin_to_countries(self.binaries))

    def __getitem__(self, item):
        return self.binaries[item]

    def __eq__(self, other):
        if isinstance(other, (list, tuple)):
            other = countries_to_bin(other)
        if isinstance(other, CountriesValue):
            other = other.binaries
        return self.binaries == other

    def __nonzero__(self):
        return self.binaries != [0, 0, 0, 0]

    def __repr__(self):
        return "%s (%s)" % (self.__class__, bin_to_countries(self.binaries))

    def __or__(self, other):
        """ Объединяет списки стран.
        :param other: список 2-х буквенных кодов стран
        :return: CountriesValues

        """
        if isinstance(other, (list, tuple)):
            other = countries_to_bin(other)
        result = [0, 0, 0, 0]
        for i in range(4):
            result[i] = self.binaries[i] | other[i]
        return CountriesValue(result)

    def __sub__(self, other):
        """ Удаляет из текущего значение переданный список стран.
        :param other список 2-х буквенных кодов стран:
        :return:

        """
        if isinstance(other, (list, tuple)):
            other = countries_to_bin(other)
        result = [0, 0, 0, 0]
        for i in range(4):
            result[i] = self.binaries[i] & ~other[i]
        return CountriesValue(result)

    def __contains__(self, item):
        """ Проверяет вхождение страны в список.
        :param item: 2-х символьный код страны для проверки
        :return: True/False

        """
        try:
            binaries = countries_to_bin([item])
        except KeyError:
            # Передана невалидная или неподдерживаемая страна
            return False
        for i in range(4):
            if binaries[i]:
                return bool(self.binaries[i] & binaries[i])
        return False


class CountriesFieldDescriptor(Creator):
    """ Управляет доступом к значениям битовых полей. """

    def __get__(self, obj, objtype=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        return CountriesValue([getattr(obj, f) for f in self.field.bit_field_names])

    def __set__(self, obj, value):
        if isinstance(value, (list, tuple)):
            value = countries_to_bin(value)
        elif isinstance(value, CountriesValue):
            value = value.binaries
        value = zip(self.field.bit_field_names, list(value))
        for f_name, binary in value:
            setattr(obj, f_name, binary)


class CountriesField(models.Field):
    """ Класс поля для хранения битовой карты стран. """

    def contribute_to_class(self, cls, name, virtual_only=True):
        super(CountriesField, self).contribute_to_class(cls, name, virtual_only=True)
        self.bit_field_names = []
        if not cls._meta.abstract:
            for i in range(0, 4):
                bit_field_name = get_bit_field_name(i, name=name)
                start = i * MAX_FLAG_COUNT
                end = i * MAX_FLAG_COUNT + MAX_FLAG_COUNT
                flags = ALL_COUNTRIES[start:end]
                bit_field = BitField(flags=flags, default=0, editable=False)
                cls.add_to_class(bit_field_name, bit_field)
                self.bit_field_names.append(bit_field_name)

        setattr(cls, name, CountriesFieldDescriptor(self))

        models.signals.pre_init.connect(self.instance_pre_init, sender=cls,
                                        weak=False)

    def instance_pre_init(self, signal, sender, args, kwargs, **opts):
        """ Обработка создания объекта модели. """
        if self.name in kwargs:
            countries = kwargs.pop(self.name)
            binaries = countries_to_bin(countries)
            kwargs.update(dict(zip(self.bit_field_names, binaries)))

    def get_attname_column(self):
        return self.get_attname(), None

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        defaults = {'form_class': CountriesFormField}
        defaults.update(kwargs)
        return super(CountriesField, self).formfield(**defaults)
