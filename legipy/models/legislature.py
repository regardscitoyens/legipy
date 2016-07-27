# coding: utf-8

from .base import LegipyModel


class Legislature(LegipyModel):
    def __init__(self, number=None, start=None, end=None):
        self.number = number
        self.start = start
        self.end = end
