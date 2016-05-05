# coding: utf-8

import requests

from ..common import servlet_url
from ..parsers import parse_pending_law_list, parse_published_law_list


class LawService:
    pub_url = servlet_url('affichLoiPubliee')
    pend_url = servlet_url('affichLoiPreparation')

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
