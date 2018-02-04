# coding: utf-8

from .base import LegipyModel


class Code(LegipyModel):
    def __init__(self, id_code, title=None, subtitle=None, date_pub=None, url_code=None):
        self.id_code = id_code
        self.title = title
        self.subtitle = subtitle
        self.date_pub = date_pub
        self.url_code = url_code
        self.children = []
