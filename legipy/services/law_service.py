# coding: utf-8

import requests

from ..common import servlet_url
from ..parsers import parse_published_law_list


class LawService:
    pub_url = servlet_url('affichLoiPubliee')
    prep_url = servlet_url('affichLoiPreparation')

    def published_laws(self, legislature):
        response = requests.get(self.pub_url,
                                params={'legislature': legislature})
        return parse_published_law_list(response.url, response.content)
