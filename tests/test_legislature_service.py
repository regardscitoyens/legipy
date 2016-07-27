# coding: utf-8

from datetime import date

from legipy.services import LegislatureService


def test_list_legislatures():
    service = LegislatureService()
    found13 = False
    found14 = False

    for leg in service.legislatures():
        if leg.number == 13:
            assert leg.start == date(2007, 6, 20)
            assert leg.end == date(2012, 6, 25)
            found13 = True

        if leg.number == 14:
            assert leg.start == date(2012, 6, 26)
            found14 = True

    assert found13
    assert found14
