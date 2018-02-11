# coding: utf-8

from .base import LegipyModel


class Code(LegipyModel):
    def __init__(self,
                 id_code,
                 title=None,
                 subtitle=None,
                 date_pub=None,
                 url_code=None):
        self.id_code = id_code
        self.title = title
        self.subtitle = subtitle
        self.date_pub = date_pub
        self.url_code = url_code
        self.children = None


class Section(LegipyModel):
    def __init__(self,
                 id_section,
                 title,
                 content=None,
                 articles=None,
                 url_section=None,
                 children=None):
        self.id_section = id_section
        self.title = title
        self.content = content
        self.articles = articles
        self.url_section = url_section
        self.children = children


class Article(LegipyModel):
    def __init__(self,
                 title,
                 history):
        self.title = title
        self.history = history
