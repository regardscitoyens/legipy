# coding: utf-8

from datetime import date


class LegipyModel:
    def to_json(self):
        d = dict()

        for k, v in self.__dict__.items():
            if v is not None:
                if isinstance(v, date):
                    d[k] = v.isoformat()
                else:
                    d[k] = v

        return d
