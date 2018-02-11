# coding: utf-8

import requests
import six

from legipy.common import page_url
from legipy.parsers.legislature_list_parser import parse_legislature_list
from legipy.services import Singleton


@six.add_metaclass(Singleton)
class LegislatureService(object):
    url = page_url('dossiers_legislatifs')
    cache = None

    @classmethod
    def legislatures(cls):
        if cls.cache is None:
            response = requests.get(cls.url)
            cls.cache = parse_legislature_list(response.url, response.content)

        return cls.cache
