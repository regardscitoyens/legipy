import datetime

import requests
import six

from legipy.common import servlet_url
from legipy.common import new_page_url
from legipy.parsers.code_parser import CodeParser
from legipy.parsers.code_parser import parser_articles
from legipy.services import Singleton


@six.add_metaclass(Singleton)
class CodeService(object):
    code_list_url = new_page_url('liste/code')
    code_url = new_page_url('codes/texte_lc/{id_code}/{date}/')

    def codes(self):
        # https://www.legifrance.gouv.fr/liste/code?etatTexte=VIGUEUR
        # NB: etatTexte cumulable, valeurs possibles: VIGUEUR, VIGUEUR_DIFF, ABROGE
        response = requests.get(
            self.code_list_url,
        )
        return CodeParser.parse_code_list(response.url, response.content)

    def code(self, id_code, date_pub, with_articles):
        # https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006075116/2021-04-28/
        date_pub = date_pub or datetime.date.today().strftime('%Y-%m-%d')
        response = requests.get(
            self.code_url.format(id_code=id_code, date=date_pub),
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
