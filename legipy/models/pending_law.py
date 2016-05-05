# coding: utf-8


class PendingLaw:
    def __init__(self, year=None, legislature=None, type=None, title=None,
                 nor=None, legi_url=None, legi_id=None):
        self.year = year
        self.legislature = legislature
        self.type = type
        self.title = title
        self.nor = nor
        self.legi_url = legi_url
        self.legi_id = legi_id
