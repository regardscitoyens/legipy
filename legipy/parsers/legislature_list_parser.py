# coding: utf-8
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup

from legipy.common import parse_date
from legipy.common import parse_roman
from legipy.models.legislature import Legislature


def parse_legislature_list(url, html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    results = []

    for leg_header in soup.find_all('h2'):
        text = leg_header.get_text()
        text = re.sub(r'\s+', ' ', text)
        num = parse_roman(re.search('^[MDCLXVI]+', text).group(0))

        m = re.search(r'à compter du (\d{1,2}(?:er)?\s+[^\s]+\s+\d{4})', text)
        if m:
            start = parse_date(m.group(1))
            end = None
        else:
            start = None
            end = None

        m = re.search(r'du (\d{1,2}(?:er)?\s+[^\s]+\s+\d{4}) '
                      r'au (\d{1,2}(?:er)?\s+[^\s]+\s+\d{4})', text)
        if m:
            start = parse_date(m.group(1))
            end = parse_date(m.group(2))

        results.append(Legislature(number=num, start=start, end=end))

    return results
