# coding: utf-8
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup

from six.moves.urllib.parse import parse_qs
from six.moves.urllib.parse import urljoin
from six.moves.urllib.parse import urlparse

from legipy.common import cleanup_url
from legipy.common import merge_spaces
from legipy.models.law import Law


def parse_common_law_list(url, html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    results = []

    div = soup.find('div', {'id': 'content_right'})
    ul = div.find('ul')

    re_find_common = re.compile(r'dite?[: ]+(?:loi )?"\s*([^"]+?)\s*"', re.I)
    re_find_second = re.compile(r'"\s*ou ((?:loi )?)"\s*([^"]+?)\s*"', re.I)

    for law_entry in ul.select('li'):
        link = law_entry.find('a')
        if not link:
            continue

        link_text = _clean_typos_legifrance(law_entry.get_text())
        nor_num = re.search(r'NOR\s*([A-Z0-9]+)\n', link_text)
        url_legi = cleanup_url(urljoin(url, link['href']))
        qs_legi = parse_qs(urlparse(url_legi).query)

        text_parts = link_text.strip("\n\r\t\s)").split('\n')
        title = merge_spaces(text_parts[0])
        common_text = merge_spaces(text_parts[-1]).strip("() ")
        try:
            common = re_find_common.search(common_text).group(1)
        except Exception:
            common = common_text
        try:
            second = re_find_second.search(common_text)
            common += " ; %s" % "".join(second.groups())
        except Exception:
            pass

        results.append(
            Law(
                title=title,
                common_name=common.replace('Loi', 'loi'),
                nor=nor_num.group(1) if nor_num else None,
                url_legi=url_legi,
                id_legi=qs_legi['cidTexte'][0]
            )
        )

    return results


def _clean_typos_legifrance(text):
    text = text.replace('loi ALUR \'', 'loi ALUR "')
    text = text.replace('El Khomry', 'loi El Khomri')
    text = text.replace('DDADUE', 'loi DDADUE')
    return text
