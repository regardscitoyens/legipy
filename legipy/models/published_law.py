# coding: utf-8


class PublishedLaw:
    def __init__(self, year=None, legislature=None, number=None, type=None,
                 pub_date=None, title=None, legi_url=None, legi_id=None):
        self.year = year
        self.legislature = legislature
        self.number = number
        self.type = type
        self.pub_date = pub_date
        self.title = title
        self.legi_url = legi_url
        self.legi_id = legi_id
