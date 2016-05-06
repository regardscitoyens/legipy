# coding: utf-8

from datetime import date
import math
import re

LEG_SECONDS = 5 * 3600 * 24 * 365
LEG_REF = 14
LEG_REF_START = date(2012, 06, 01)


def _current_legislature():
    delta = date.today() - LEG_REF_START
    return int(LEG_REF + math.floor(delta.total_seconds() / LEG_SECONDS))


LEG_CURRENT = _current_legislature()

DOMAIN = 'www.legifrance.gouv.fr'

MONTHS = [
    'janvier',
    u'février',
    'mars',
    'avril',
    'mai',
    'juin',
    'juillet',
    u'août',
    'septembre',
    'octobre',
    'novembre',
    u'décembre'
]

LAW_KINDS = [
    'organique',
    'constitutionnelle'
]


def servlet_url(servlet):
    return 'http://%s/%s.do' % (DOMAIN, servlet)


def cleanup_url(url):
    return re.sub(r';jsessionid=[^\?]+\?', '?', url)


def merge_spaces(string):
    return re.sub('\s+', ' ', string)


def parse_date(string):
    match = re.match(r'(\d{1,2})(?:er)?\s+([^\s]+)\s+(\d{4})', string)

    if not match:
        return None

    try:
        month = 1 + MONTHS.index(match.group(2))
    except:
        return None

    return date(int(match.group(3)), month, int(match.group(1)))
