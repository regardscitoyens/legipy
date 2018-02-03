# coding: utf-8

from bs4 import BeautifulSoup
import re

from six.moves.urllib.parse import urljoin, urlparse, parse_qs

from ..common import cleanup_url, merge_spaces
from ..models import Law


def parse_pending_law_list(url, html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    results = []

    for year_header in soup.find_all('h3'):
        year = int(year_header.get_text())
        ul = year_header.find_next_sibling('ul')

        if not ul:
            continue

        for law_entry in ul.select('li a'):
            link_text = law_entry.get_text()
            nor_num = re.search('\(([A-Z0-9]+)\)$', link_text)

            url_legi = cleanup_url(urljoin(url, law_entry['href']))
            qs_legi = parse_qs(urlparse(url_legi).query)

            results.append(Law(
                year=year,
                legislature=int(qs_legi['legislature'][0]),
                type=qs_legi['typeLoi'][0],
                title=merge_spaces(link_text),
                nor=nor_num.group(1) if nor_num else None,
                url_legi=url_legi,
                id_legi=qs_legi['idDocument'][0]
            ))

    return results
