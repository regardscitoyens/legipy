# coding: utf-8

from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse, parse_qs

from ..common import cleanup_url, merge_spaces
from ..models import Law


def parse_common_law_list(url, html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    results = []

    div = soup.find('div', {'id': 'content_right'})
    ul = div.find('ul')

    for law_entry in ul.select('li'):
        link = law_entry.find('a')
        if not link:
            continue

        link_text = _clean_typos_legifrance(law_entry.get_text())
        nor_num = re.search(r'NOR\s*([A-Z0-9]+)\n', link_text)
        title = link_text.split('NOR')[0].strip() if nor_num else link_text

        url_legi = cleanup_url(urljoin(url, link['href']))
        qs_legi = parse_qs(urlparse(url_legi).query)
        #print(link_text, nor_num, url_legi, qs_legi)

        results.append(Law(
            title=title,
            common_name=merge_spaces(link_text),
            nor=nor_num.group(1) if nor_num else None,
            url_legi=url_legi,
            id_legi=qs_legi['cidTexte'][0]
        ))

    return results

def _clean_typos_legifrance(text):
    text = text.replace('Ek Khomry', 'El Khomry')
    return text
