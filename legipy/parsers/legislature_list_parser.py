# coding: utf-8
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import re

from ..common import parse_date, parse_roman
from ..models import Legislature


def parse_legislature_list(url, html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    results = []

    for leg_header in soup.find_all('h3'):
        text = leg_header.get_text()
        num = parse_roman(re.search('^[MDCLXVI]+', text).group(0))

        m = re.search(r'A compter du (\d{1,2}(?:er)?\s+[^\s]+\s+\d{4})', text)
        if m:
            start = parse_date(m.group(1))
            end = None

        m = re.search(r'du (\d{1,2}(?:er)?\s+[^\s]+\s+\d{4}) '
                      r'au (\d{1,2}(?:er)?\s+[^\s]+\s+\d{4})', text)
        if m:
            start = parse_date(m.group(1))
            end = parse_date(m.group(2))

        results.append(Legislature(number=num, start=start, end=end))

    return results
