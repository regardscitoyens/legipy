# coding: utf-8


class LegipyModel(object):
    def to_json(self):
        d = dict()
        for k, v in self.__dict__.items():
            if v is not None:
                d[k] = v
        return d
