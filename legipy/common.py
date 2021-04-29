# coding: utf-8

import datetime
import re
from bs4.element import Tag

DOMAIN = 'www.legifrance.gouv.fr'

MONTHS = [
    u'janvier',
    u'février',
    u'mars',
    u'avril',
    u'mai',
    u'juin',
    u'juillet',
    u'août',
    u'septembre',
    u'octobre',
    u'novembre',
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


def page_url(page):
    return 'https://%s/%s' % (DOMAIN, page)


def cleanup_url(url):
    return re.sub(r';jsessionid=[^?]+\?', '?', url)


def merge_spaces(string):
    return re.sub(r'\s+', ' ', string)


def parse_date(string):
    match = re.match(r'(\d{1,2})(?:er)?\s+([^\s]+)\s+(\d{4})', string)

    if not match:
        return None

    try:
        month = 1 + MONTHS.index(match.group(2))
    except ValueError:
        # not in list
        return None

    return datetime.date(int(match.group(3)), month, int(match.group(1)))


def parse_roman(string):
    string = string.upper()
    total = 0

    for c in string:
        if c not in ROMAN_VALUES:
            raise ValueError("Not a roman numeral: %s" % string)

    for index in range(len(string)):
        value = ROMAN_VALUES[string[index]]
        if index < len(string) - 1 and ROMAN_VALUES[string[index + 1]] > value:
            total -= value
        else:
            total += value

    return total


def find_all_non_nested(parent, *args, **kwargs):
    """ find_all for non-nested elements

    I.e. the same semantics as find_all(..., recursive=True),
    except we don’t search children of matched nodes
    """
    # Indulge python 2 ?
    bfs = kwargs.pop('bfs', False)
    kwargs['recursive'] = False

    search = [parent]
    found = []
    while search:
        node = search.pop(0 if bfs else -1)
        found_at_node = node.find_all(*args, **kwargs)
        found += found_at_node
        search.extend(child for child in node.children if (
            isinstance(child, Tag) and child not in found_at_node
        ))

    return found
