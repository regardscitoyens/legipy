# coding: utf-8
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup
from six.moves.urllib.parse import urljoin

from legipy.common import cleanup_url
from legipy.common import parse_date
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
    def parse_code_list(cls, html):
        soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
        form = soup.find('form', attrs={'action': '/rechCodeArticle.do'})
        select = form.find('select', attrs={'name': 'cidTexte'})
        return [Code(option.attrs['value'], option.get_text())
                for option in select.find_all('option')
                if option.attrs['value'] != '*']

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

        # -- main text
        div = (soup
               .find('div', id='content_false')
               .find('div', attrs={'class': 'data'}))

        code = Code(self.id_code,
                    date_pub=self.date_pub,
                    url_code=cleanup_url(url))

        # -- Code title/subtitle
        div_title = div.find('div', id='titreTexte')
        span_subtitle = div_title.find('span',
                                       attrs={'class': 'sousTitreTexte'})
        if span_subtitle:
            code.title = div_title.text.replace(span_subtitle.text, '')
            code.subtitle = span_subtitle.text.strip()
            regex = r'Version consolidée au (\d{1,2}(?:er)?\s+[^\s]+\s+\d{4})'
            m = re.search(regex, code.subtitle)
            if m:
                code.date_pub = parse_date(m.group(1))

        code.title = code.title.strip()

        # -- TOC
        code.children = [self.parse_code_ul(url, child)
                         for child in div.find_all('ul', recursive=False)]

        return code

    def parse_code_ul(self, url, ul):
        """Fill the toc item"""
        li_list = ul.find_all('li', recursive=False)
        li = li_list[0]
        span_title = li.find('span',
                             attrs={'class': re.compile(r'TM\d+Code')},
                             recursive=False)

        section = Section(span_title.attrs['id'], span_title.text.strip())
        div_italic = li.find('div', attrs={'class': 'italic'}, recursive=False)
        if div_italic:
            section.content = div_italic.text.strip()
        span_link = li.find('span',
                            attrs={'class': 'codeLienArt'},
                            recursive=False)
        if span_link:
            a_link = span_link.find('a', recursive=False)
            if self.with_articles:
                service = self.section_service
                section.articles = service.articles(self.id_code,
                                                    section.id_section,
                                                    self.date_pub)
            else:
                section.articles = a_link.text.strip()
            section.url_section = cleanup_url(
                urljoin(url, a_link.attrs['href']))
        section.children = [self.parse_code_ul(url, child)
                            for child in li.find_all('ul', recursive=False)]
        return section


def parser_articles(html):
    soup = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    div = (soup
           .find('div', id='content_false')
           .find('div', attrs={'class': 'data'}))
    div_list = div.find_all('div', attrs={'class': 'article'}, recursive=False)
    articles = []
    for div_article in div_list:
        div_title = div_article.find('div',
                                     attrs={'class': 'titreArt'},
                                     recursive=False)
        title = div_title.text
        a_link = div_title.find('a')
        if a_link:
            title = title.replace(a_link.text, '')
        title = title.strip()
        div_history = div_article.find_all('div',
                                           attrs={'class': 'histoArt'},
                                           recursive=False)
        article = Article(title,
                          [(entry.find('a') or entry.find('span')).text
                           for entry in div_history])
        articles.append(article)
    return articles
