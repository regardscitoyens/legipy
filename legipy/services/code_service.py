import datetime
import requests

from legipy.common import servlet_url
from legipy.models.code import Code
from legipy.parsers.code_parser import parse_code_list
from legipy.parsers.code_parser import parse_code


class CodeService(object):
    code_list_url = servlet_url('initRechCodeArticle')
    code_url = servlet_url('affichCode')

    def codes(self):
        # https://www.legifrance.gouv.fr/initRechCodeArticle.do
        response = requests.get(
            self.code_list_url,
        )
        return parse_code_list(response.url, response.content)

    def code(self, id_code, date_pub):
        # https://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006074228&dateTexte=20180203
        date_pub = date_pub or datetime.date.today().strftime('%Y%m%d')
        response = requests.get(
            self.code_url,
            params={
                'cidTexte': id_code,
                'dateTexte': date_pub
            }
        )
        return parse_code(id_code, date_pub, response.url, response.content)
