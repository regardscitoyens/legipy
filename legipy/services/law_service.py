# coding: utf-8

import requests
import six

from legipy.common import servlet_url
from legipy.parsers.law_parser import parse_law
from legipy.parsers.common_law_list_parser import parse_common_law_list
from legipy.parsers.pending_law_list_parser import parse_pending_law_list
from legipy.parsers.published_law_list_parser import parse_published_law_list
from legipy.services import Singleton


@six.add_metaclass(Singleton)
class LawService(object):
    pub_url = servlet_url('affichLoiPubliee')
    pend_url = servlet_url('affichLoiPreparation')
    comm_url = servlet_url('affichSarde')

    def pending_laws(self, legislature, government=True):
        response = requests.get(
            self.pend_url,
            params={
                'legislature': legislature,
                'typeLoi': 'proj' if government else 'prop'
            }
        )
        return parse_pending_law_list(response.url, response.content)

    def published_laws(self, legislature):
        response = requests.get(
            self.pub_url,
            params={'legislature': legislature}
        )
        return parse_published_law_list(response.url, response.content)

    def common_laws(self):
        laws = True
        common_laws = []
        page = 1
        while laws:
            response = requests.get(
                self.comm_url,
                params={
                    'idSarde': 'SARDOBJT000007106573',
                    'reprise': 'true',
                    'page': page
                }
            )
            laws = parse_common_law_list(response.url, response.content)
            common_laws += laws
            page += 1
        return common_laws

    def get_law(self, id_legi):
        response = requests.get(
            self.pub_url,
            params={
                'idDocument': id_legi,
                'type': 'general'
            }
        )
        return parse_law(response.url, response.content, id_legi)
