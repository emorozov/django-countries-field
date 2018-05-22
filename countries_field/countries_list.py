# -*- coding: utf-8 -*-
from django.conf import settings

from .bitfield.models import MAX_FLAG_COUNT

# Порядок и количество стран заданы жестко для совместимости в случае
# обовления pycountry
ALPHA2_INDEX = [
    u'AF', u'AX', u'AL', u'DZ', u'AS', u'AD', u'AO', u'AI', u'AQ',
    u'AG', u'AR', u'AM', u'AW', u'AU', u'AT', u'AZ', u'BS', u'BH',
    u'BD', u'BB', u'BY', u'BE', u'BZ', u'BJ', u'BM', u'BT', u'BO',
    u'BQ', u'BA', u'BW', u'BV', u'BR', u'IO', u'BN', u'BG', u'BF',
    u'BI', u'KH', u'CM', u'CA', u'CV', u'KY', u'CF', u'TD', u'CL',
    u'CN', u'CX', u'CC', u'CO', u'KM', u'CG', u'CD', u'CK', u'CR',
    u'CI', u'HR', u'CU', u'CW', u'CY', u'CZ', u'DK', u'DJ', u'DM',
    u'DO', u'EC', u'EG', u'SV', u'GQ', u'ER', u'EE', u'ET', u'FK',
    u'FO', u'FJ', u'FI', u'FR', u'GF', u'PF', u'TF', u'GA', u'GM',
    u'GE', u'DE', u'GH', u'GI', u'GR', u'GL', u'GD', u'GP', u'GU',
    u'GT', u'GG', u'GN', u'GW', u'GY', u'HT', u'HM', u'VA', u'HN',
    u'HK', u'HU', u'IS', u'IN', u'ID', u'IR', u'IQ', u'IE', u'IM',
    u'IL', u'IT', u'JM', u'JP', u'JE', u'JO', u'KZ', u'KE', u'KI',
    u'KP', u'KR', u'KW', u'KG', u'LA', u'LV', u'LB', u'LS', u'LR',
    u'LY', u'LI', u'LT', u'LU', u'MO', u'MK', u'MG', u'MW', u'MY',
    u'MV', u'ML', u'MT', u'MH', u'MQ', u'MR', u'MU', u'YT', u'MX',
    u'FM', u'MD', u'MC', u'MN', u'ME', u'MS', u'MA', u'MZ', u'MM',
    u'NA', u'NR', u'NP', u'NL', u'NC', u'NZ', u'NI', u'NE', u'NG',
    u'NU', u'NF', u'MP', u'NO', u'OM', u'PK', u'PW', u'PS', u'PA',
    u'PG', u'PY', u'PE', u'PH', u'PN', u'PL', u'PT', u'PR', u'QA',
    u'RE', u'RO', u'RU', u'RW', u'BL', u'SH', u'KN', u'LC', u'MF',
    u'PM', u'VC', u'WS', u'SM', u'ST', u'SA', u'SN', u'RS', u'SC',
    u'SL', u'SG', u'SX', u'SK', u'SI', u'SB', u'SO', u'ZA', u'GS',
    u'ES', u'LK', u'SD', u'SR', u'SS', u'SJ', u'SZ', u'SE', u'CH',
    u'SY', u'TW', u'TJ', u'TZ', u'TH', u'TL', u'TG', u'TK', u'TO',
    u'TT', u'TN', u'TR', u'TM', u'TC', u'TV', u'UG', u'UA', u'AE',
    u'GB', u'US', u'UM', u'UY', u'UZ', u'VU', u'VE', u'VN', u'VG',
    u'VI', u'WF', u'EH', u'YE', u'ZM', u'ZW'
]


EXTRA_COUNTRIES = getattr(settings, 'EXTRA_COUNTRIES', [])

if EXTRA_COUNTRIES:
    gap = 4 * MAX_FLAG_COUNT - len(ALPHA2_INDEX) - len(EXTRA_COUNTRIES)
    assert(gap == 0), "count of extra countres can be only {}"\
        .format(4 * MAX_FLAG_COUNT - len(ALPHA2_INDEX))

ALL_COUNTRIES = ALPHA2_INDEX +  [c[0] if c else None for c in EXTRA_COUNTRIES]
