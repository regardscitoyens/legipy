# coding: utf-8
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup

from legipy.common import LAW_KINDS
from legipy.common import cleanup_url
from legipy.common import merge_spaces
from legipy.common import parse_date
from legipy.models.law import Law


def parse_law(url, html, id_legi):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    law = Law(
        url_legi=cleanup_url(url),
        id_legi=id_legi
    )

    clean_title = merge_spaces(soup.h2.get_text()).strip()
    law.title = re.sub(r'^Dossiers législatifs( - )?', '', clean_title).strip()

    if len(law.title) == 0:
        return None

    title_remain = None
    law_num = re.match(r'LOI\s+(?:([^\s]+)\s+)?n°\s+([^\s]+)(.*)', law.title,
                       re.I)
    if law_num:
        law.type = 'law'
        law.kind = law_num.group(1)
        law.number = law_num.group(2)
        title_remain = law_num.group(3)

    prop = re.match('(proj|prop)(?:et de loi|osition de loi) (\w+)', law.title,
                    re.I)
    if prop:
        law.type = prop.group(1).lower()

        try:
            LAW_KINDS.index(prop.group(2))
            law.kind = prop.group(2)
        except ValueError:
            # not in list
            law.kind = None

    if title_remain:
        pub_date = re.match(r'\s*du\s+(\d{1,2}(?:er)?\s+[^\s]+\s+\d{4})',
                            title_remain)

        if pub_date:
            law.pub_date = parse_date(pub_date.group(1))

    dos_senat = soup.find(lambda e: e.name == 'a' and (
            re.search(r'/dossier-legislatif/', e['href']) or
            re.search(r'/dossierleg/', e['href'])))
    if dos_senat:
        law.url_senat = dos_senat['href'].split('#')[0]
        law.id_senat = re.search(r'([^/]+)\.html$', law.url_senat).group(1)

    dos_an = soup.find(lambda e: e.name == 'a' and
                       re.search(r'/dossiers/', e['href']))

    if dos_an:
        law.url_an = dos_an['href'].split('#')[0]
        law.legislature = int(re.search(r'/(\d+)/dossiers/',
                                        law.url_an).group(1))
        law.id_an = re.search(r'([^/]+)\.asp$', law.url_an).group(1)

    return law
