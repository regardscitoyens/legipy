# coding: utf-8

import requests

from ..common import page_url
from ..parsers import parse_legislature_list


class LegislatureService:
    url = page_url('dossiers_legislatifs')
    cache = None

    @classmethod
    def legislatures(cls):
        if cls.cache is None:
            response = requests.get(cls.url)
            cls.cache = parse_legislature_list(response.url, response.content)

        return cls.cache
