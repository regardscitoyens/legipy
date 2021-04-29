# coding: utf-8
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup
from six.moves.urllib.parse import urljoin, urldefrag

from legipy.common import find_all_non_nested
from legipy.common import cleanup_url
from legipy.common import parse_date
from legipy.common import merge_spaces
from legipy.models.code import Article
from legipy.models.code import Code
from legipy.models.code import Section


class CodeParser(object):
    def __init__(self, id_code, date_pub, with_articles):
        """
        Construct the parser.

        :type  id_code: str
        :param id_code: Code ID

        :type  date_pub: str
        :param date_pub: Code Date

        :type  with_articles: bool
        :param with_articles: Show details for each articles
        """
        self.id_code = id_code
        self.date_pub = date_pub
        self.with_articles = with_articles
        self._section_service = None

    @property
    def section_service(self):
        if self._section_service is None:
            from legipy.services.code_service import SectionService

            self._section_service = SectionService()
        return self._section_service

    @classmethod
    def parse_code_list(cls, url, html):
        soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
        codes = [code.find('a') for code in soup.find_all('h2')]
        return [Code(re.sub('^id', '', code.attrs['id']),
                     code.get_text().strip(),
                     url_code=urljoin(url, code.attrs['href']))
                for code in codes if code is not None]

    def parse_code(self, url, html):
        """
        Parse the code details and TOC from the given HTML content

        :type  url: str
        :param url: source URL of the page

        :type  html: unicode
        :param html: Content of the HTML

        :return: the code
        """
        soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

        code = Code(self.id_code,
                    date_pub=self.date_pub,
                    url_code=cleanup_url(url))

        # -- Code title/subtitle
        code.title = soup.h1.text.strip()
        code.subtitle = soup.find('div', {'class': 'vigor-title'}).text.strip()
        regex = (r'Version (?:en vigueur au|abrogée depuis le) '
                 r'(\d{1,2}(?:er)?\s+[^\s]+\s+\d{4})')
        m = re.search(regex, code.subtitle)
        if m:
            code.date_pub = parse_date(m.group(1))

        # -- TOC
        toc = soup.find('ul', id='liste-sommaire')
        code.children = [self.parse_toc_element(url, partie)
                         for partie in toc.find_all('li', recursive=False)]

        return code

    def parse_toc_element(self, url, li):
        """Fill the toc item"""
        a_link = li.find('a', attrs={'class': 'articleLink'}, recursive=False)

        if a_link:
            # cleanup_url(urljoin(url, a_link.attrs['href']))
            return Article(a_link.text.strip(), None,
                           re.sub('^art', '', a_link.attrs['id']))

        title = li.find(['span', 'a'], attrs={'class': 'title-link'},
                        recursive=False)

        match = re.match(r'(.*?)(?: \((Articles .*)\))?$',
                         merge_spaces(title.text.strip()))
        title_text, articles = match.groups()

        section = Section(title.attrs['id'], title_text)

        if 'href' in title.attrs:
            section_url = urldefrag(urljoin(url, title.attrs['href']))[0]
            section.url_section = urljoin(url, section_url)

        for ul in find_all_non_nested(li, 'ul'):
            for child_node in ul.find_all('li', recursive=False):
                child = self.parse_toc_element(url, child_node)
                if isinstance(child, Article) and self.with_articles:
                    if section.articles is None:
                        section.articles = []
                    section.articles.append(child)
                elif isinstance(child, Section):
                    if section.children is None:
                        section.children = []
                    section.children.append(child)

        if not section.children and not self.with_articles:
            section.articles = articles

        return section


def parser_articles(url, html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    articles = []
    for article in soup.find_all('article'):
        # Articles abrogés en h3
        title = article.find(['h2', 'h3'])

        # or title.attrs['data-anchor']
        article_id = re.sub('(-[0-9])*$', '', title.attrs['id'])

        # Only last modification
        history = article.find('p', attrs={'class': 'date'})
        history = history.text.strip() if history else None

        articles.append(Article(title.text.strip(), history, article_id))
    return articles
