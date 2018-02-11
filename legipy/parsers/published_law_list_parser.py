# coding: utf-8
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup

from six.moves.urllib.parse import parse_qs
from six.moves.urllib.parse import urljoin
from six.moves.urllib.parse import urlparse

from legipy.common import cleanup_url
from legipy.common import merge_spaces
from legipy.common import parse_date
from legipy.models.law import Law


def parse_published_law_list(url, html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    results = []

    for year_header in soup.find_all('h3'):
        year = int(year_header.get_text())
        ul = year_header.find_next_sibling('ul')

        if not ul:
            continue

        for law_entry in ul.select('li a'):
            link_text = law_entry.get_text()
            law_num = re.match(r'LOI\s+(?:([^\s]+)\s+)?n°\s+([^\s]+)',
                               link_text, re.I)

            if not law_num:
                continue

            url_legi = cleanup_url(urljoin(url, law_entry['href']))
            qs_legi = parse_qs(urlparse(url_legi).query)

            title = law_entry.next_sibling
            pub_date = re.match(r'\s*du\s+(\d{1,2}(?:er)?\s+[^\s]+\s+\d{4})',
                                title)

            results.append(Law(
                year=year,
                legislature=int(qs_legi['legislature'][0]),
                number=law_num.group(2),
                type='law',
                kind=law_num.group(1),
                pub_date=parse_date(pub_date.group(1)) if pub_date else None,
                title=merge_spaces(link_text + title),
                url_legi=url_legi,
                id_legi=qs_legi['idDocument'][0]
            ))

    return results
