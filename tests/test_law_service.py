# coding: utf-8

from datetime import date

from legipy.services import LawService


def test_published_laws():
    service = LawService()
    laws = service.published_laws(13)

    assert 261 == len(laws)

    assert laws[0].year == 2012
    assert laws[0].legislature == 13
    assert laws[0].type is None
    assert laws[0].number == '2012-410'
    assert laws[0].legi_url == 'https://www.legifrance.gouv.fr/affichLoiPubliee.do?idDocument=JORFDOLE000024106525&type=general&legislature=13'
    assert laws[0].legi_id == 'JORFDOLE000024106525'
    assert laws[0].pub_date == date(2012, 3, 27)
    assert laws[0].title == u'LOI n° 2012-410 du 27 mars 2012  relative à la protection de l\'identité'

    assert laws[19].type == 'organique'


def test_pending_law_proposals():
    service = LawService()
    laws = service.pending_laws(13, False)

    assert 71 == len(laws)

    assert laws[0].year == 2012
    assert laws[0].legislature == 13
    assert laws[0].type == 'prop'
    assert laws[0].legi_url == 'https://www.legifrance.gouv.fr/affichLoiPreparation.do?idDocument=JORFDOLE000025450258&type=general&typeLoi=prop&legislature=13'
    assert laws[0].legi_id == 'JORFDOLE000025450258'
    assert laws[0].title == u'Proposition de loi tendant à renforcer l\'effectivité de la peine complémentaire d\'interdiction du territoire français et visant à réprimer les délinquants réitérants'


def test_pending_law_projects():
    service = LawService()
    laws = service.pending_laws(13, True)

    assert 99 == len(laws)

    assert laws[0].year == 2012
    assert laws[0].legislature == 13
    assert laws[0].type == 'proj'
    assert laws[0].nor is None
    assert laws[0].legi_url == 'https://www.legifrance.gouv.fr/affichLoiPreparation.do?idDocument=JORFDOLE000026052216&type=general&typeLoi=proj&legislature=13'
    assert laws[0].legi_id == 'JORFDOLE000026052216'
    assert laws[0].title == u'Projet de loi ratifiant l’ordonnance n° 2011-1923 du 22 décembre 2011 relative à l\'évolution de la sécurité sociale à Mayotte dans le cadre de la départementalisation'

    assert laws[1].nor == 'DEVA1208027L'
