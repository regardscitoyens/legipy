# coding: utf-8

from datetime import date

from legipy.services import LawService


def test_published_laws():
    service = LawService()
    laws = service.published_laws(13)

    assert 261 == len(laws)

    assert laws[0].year == 2012
    assert laws[0].type is None
    assert laws[0].number == '2012-410'
    assert laws[0].legi_url == 'https://www.legifrance.gouv.fr/affichLoiPubliee.do?idDocument=JORFDOLE000024106525&type=general&legislature=13'
    assert laws[0].legi_id == 'JORFDOLE000024106525'
    assert laws[0].pub_date == date(2012, 3, 27)
    assert laws[0].title == u'LOI n° 2012-410 du 27 mars 2012  relative à la protection de l\'identité'

    assert laws[19].type == 'organique'
