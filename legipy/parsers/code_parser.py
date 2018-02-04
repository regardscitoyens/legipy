# coding: utf-8
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup
from six.moves.urllib.parse import urljoin

from legipy.common import cleanup_url
from legipy.models.code import Code

if False:
    # for type hints
    import bs4.element.Tag


def parse_code_list(url, html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

    form = soup.find('form', attrs={'action': '/rechCodeArticle.do'})
    select = form.find('select', attrs={'name': 'cidTexte'})

    return [Code(option.attrs['value'], option.get_text())
            for option in select.find_all('option')
            if option.attrs['value'] != '*']


def parse_code_ul(url, ul):
    """Fill the toc item"""
    # type: (bs4.element.Tag) -> dict
    li_list = ul.find_all('li', recursive=False)
    li = li_list[0]  # type: bs4.element.Tag
    span_title = li.find('span', attrs={'class': re.compile(r'TM\d+Code')}, recursive=False)
    item = dict()
    item['title'] = span_title.text.strip()
    item['id_section'] = span_title.attrs['id']
    div_italic = li.find('div', attrs={'class': 'italic'}, recursive=False)
    if div_italic:
        item['content'] = div_italic.text.strip()
    span_link = li.find('span', attrs={'class': 'codeLienArt'}, recursive=False)
    if span_link:
        a_link = span_link and span_link.find('a', recursive=False)  # type: bs4.element.Tag
        item['articles'] = a_link.text.strip()
        item['url_section'] = cleanup_url(urljoin(url, a_link.attrs['href']))
    item['children'] = [parse_code_ul(url, child)
                        for child in li.find_all('ul', recursive=False)]
    return item


def parse_code(id_code, date_pub, url, html):
    """
    Parse the code details and TOC from the given HTML content

    :type  id_code: str
    :param id_code: Code ID

    :type  date_pub: str
    :param date_pub: Code Date

    :type  url: str
    :param url: source URL of the page

    :type  html: unicode
    :param html: Content of the HTML

    :return: the code
    """
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

    # -- main text
    div = soup.find('div', id='content_false').find('div', attrs={'class': 'data'})

    code = Code(id_code, date_pub=date_pub, url_code=cleanup_url(url))

    # -- Code title/subtitle
    div_title = div.find('div', id='titreTexte')  # type: bs4.element.Tag
    span_subtitle = div_title.find('span', attrs={'class': 'sousTitreTexte'})
    if span_subtitle:
        code.title = div_title.text.replace(span_subtitle.text, '')
    code.subtitle = span_subtitle.text.strip()
    code.title = code.title.strip()

    # -- TOC
    code.children = [parse_code_ul(url, child)
                     for child in div.find_all('ul', recursive=False)]

    return code
