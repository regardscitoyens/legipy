# coding: utf-8

from datetime import date
import re

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


def servlet_url(servlet):
    return 'http://%s/%s.do' % (DOMAIN, servlet)


def cleanup_url(url):
    return re.sub(r';jsessionid=[^\?]+\?', '?', url)


def parse_date(string):
    match = re.match(r'(\d{1,2})(?:er)?\s+([^\s]+)\s+(\d{4})', string)

    if not match:
        return None

    try:
        month = 1 + MONTHS.index(match.group(2))
    except:
        return None

    return date(int(match.group(3)), month, int(match.group(1)))
