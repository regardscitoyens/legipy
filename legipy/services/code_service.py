import datetime

import requests
import six

from legipy.common import servlet_url
from legipy.parsers.code_parser import CodeParser
from legipy.parsers.code_parser import parser_articles
from legipy.services import Singleton


@six.add_metaclass(Singleton)
class CodeService(object):
    code_list_url = servlet_url('initRechCodeArticle')
    code_url = servlet_url('affichCode')

    def codes(self):
        # https://www.legifrance.gouv.fr/initRechCodeArticle.do
        response = requests.get(
            self.code_list_url,
        )
        return CodeParser.parse_code_list(response.content)

    def code(self, id_code, date_pub, with_articles):
        # https://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006074228&dateTexte=20180203
        date_pub = date_pub or datetime.date.today().strftime('%Y%m%d')
        response = requests.get(
            self.code_url,
            params={
                'cidTexte': id_code,
                'dateTexte': date_pub
            }
        )
        parser = CodeParser(id_code, date_pub, with_articles=with_articles)
        return parser.parse_code(response.url, response.content)


@six.add_metaclass(Singleton)
class SectionService(object):
    section_url = servlet_url('affichCode')

    def articles(self, id_code, id_section, date_pub):
        # https://www.legifrance.gouv.fr/affichCode.do?idSectionTA=LEGISCTA000006175632&cidTexte=LEGITEXT000006074075&dateTexte=20180210
        date_pub = date_pub or datetime.date.today().strftime('%Y%m%d')
        response = requests.get(
            self.section_url,
            params={
                'cidTexte': id_code,
                'dateTexte': date_pub,
                'idSectionTA': id_section
            }
        )
        return parser_articles(response.content)
