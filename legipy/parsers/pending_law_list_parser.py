# coding: utf-8

from bs4 import BeautifulSoup
import re
from urlparse import urljoin, urlparse, parse_qs

from ..common import cleanup_url
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

            legi_url = cleanup_url(urljoin(url, law_entry['href']))
            legi_qs = parse_qs(urlparse(legi_url).query)

            results.append(Law(
                year=year,
                legislature=int(legi_qs['legislature'][0]),
                type=legi_qs['typeLoi'][0],
                title=link_text,
                nor=nor_num.group(1) if nor_num else None,
                legi_url=legi_url,
                legi_id=legi_qs['idDocument'][0]
            ))

    return results
