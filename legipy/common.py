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

LAW_KINDS = [
    'organique',
    'constitutionnelle'
]

ROMAN_VALUES = {
    'M': 1000,
    'D': 500,
    'C': 100,
    'L': 50,
    'X': 10,
    'V': 5,
    'I': 1
}


def servlet_url(servlet):
    return 'http://%s/%s.do' % (DOMAIN, servlet)


def page_url(page):
    return 'http://%s/%s.jsp' % (DOMAIN, page)


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


def parse_roman(string):
    string = string.upper()
    total = 0

    for c in string:
        if c not in ROMAN_VALUES:
            raise ValueError("Not a roman numeral: %s" % string)

    for index in range(len(string)):
        value = ROMAN_VALUES[string[index]]
        if index < len(string) - 1 and ROMAN_VALUES[string[index+1]] > value:
            total -= value
        else:
            total += value

    return total
