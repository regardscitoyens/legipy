# coding: utf-8
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup
from six.moves.urllib.parse import parse_qs
from six.moves.urllib.parse import urljoin
from six.moves.urllib.parse import urlparse

from legipy.common import cleanup_url
from legipy.common import merge_spaces
from legipy.common import LAW_KINDS
from legipy.models.law import Law


def parse_pending_law_list(url, html, **law_kwargs):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    results = []

    for year_header in soup.find_all('h2'):
        year = int(year_header.get_text().strip())
        ul = year_header.find_next('ul')

        if not ul:
            continue

        for law_entry in ul.select('li a'):
            link_text = law_entry.get_text().strip()
            nor_num = re.search(r'\(([A-Z0-9]+)\)$', link_text)

            type_loi = re.match(r'(Projet|Proposition)\s+de\s+loi\s+({})?'\
                                .format('|'.join(LAW_KINDS)), link_text)
            if type_loi:
                print(type_loi.groups())

            url_legi = cleanup_url(urljoin(url, law_entry['href']))
            id_legi = urlparse(url_legi).path.strip('/').split('/')[-1]

            results.append(Law(
                year=year,
                id_legi=id_legi,
                type=type_loi.group(0).lower()[:4],
                kind=type_loi.group(1),
                title=merge_spaces(link_text),
                nor=nor_num.group(1) if nor_num else None,
                url_legi=url_legi,
                **law_kwargs
            ))

    return results
