# coding: utf-8

from datetime import date

import vcr

from legipy.services.law_service import LawService


recorder = vcr.VCR(cassette_library_dir='tests/fixtures/cassettes')

@recorder.use_cassette()
def test_list_published_laws():
    service = LawService()
    laws = service.published_laws(13)

    assert 261 == len(laws)

    assert laws[0].year == 2012
    assert laws[0].legislature == 13
    assert laws[0].type == 'law'
    assert laws[0].kind is None
    assert laws[0].number == '2012-410'
    assert laws[0].url_legi == 'https://www.legifrance.gouv.fr/affichLoiPubliee.do?idDocument=JORFDOLE000024106525&type=general&legislature=13'
    assert laws[0].id_legi == 'JORFDOLE000024106525'
    assert laws[0].pub_date == date(2012, 3, 27)
    assert laws[0].title == u'LOI n° 2012-410 du 27 mars 2012 relative à la protection de l\'identité'

    assert laws[19].kind == 'organique'


@recorder.use_cassette()
def test_published_law():
    service = LawService()
    law = service.get_law('JORFDOLE000024106525')

    assert law.legislature == 13
    assert law.type == 'law'
    assert law.kind is None
    assert law.number == '2012-410'
    assert law.url_an == 'http://www.assemblee-nationale.fr/13/dossiers/protection_identite.asp'
    assert law.id_an == 'protection_identite'
    assert law.url_legi == 'https://www.legifrance.gouv.fr/affichLoiPubliee.do?idDocument=JORFDOLE000024106525&type=general'
    assert law.url_senat == 'http://www.senat.fr/dossier-legislatif/ppl09-682.html'
    assert law.id_senat == 'ppl09-682'
    assert law.id_legi == 'JORFDOLE000024106525'
    assert law.pub_date == date(2012, 3, 27)
    assert law.title == u'LOI n° 2012-410 du 27 mars 2012 relative à la protection de l\'identité'


@recorder.use_cassette()
def test_list_pending_law_proposals():
    service = LawService()
    laws = service.pending_laws(13, False)

    assert 71 == len(laws)

    assert laws[0].year == 2012
    assert laws[0].legislature == 13
    assert laws[0].type == 'prop'
    assert laws[0].url_legi == 'https://www.legifrance.gouv.fr/affichLoiPreparation.do?idDocument=JORFDOLE000025450258&type=general&typeLoi=prop&legislature=13'
    assert laws[0].id_legi == 'JORFDOLE000025450258'
    assert laws[0].title == u'Proposition de loi tendant à renforcer l\'effectivité de la peine complémentaire d\'interdiction du territoire français et visant à réprimer les délinquants réitérants'


@recorder.use_cassette()
def test_pending_law_proposal():
    service = LawService()
    law = service.get_law('JORFDOLE000025450258')

    assert law.legislature == 13
    assert law.type == 'prop'
    assert law.kind is None
    assert law.number is None
    assert law.url_an == 'http://www.assemblee-nationale.fr/13/dossiers/interdiction_territoire_delinquants_reiterants.asp'
    assert law.id_an == 'interdiction_territoire_delinquants_reiterants'
    assert law.url_legi == 'https://www.legifrance.gouv.fr/affichLoiPubliee.do?idDocument=JORFDOLE000025450258&type=general'
    assert law.id_legi == 'JORFDOLE000025450258'
    assert law.url_senat == 'http://www.senat.fr/dossier-legislatif/ppl11-466.html'
    assert law.id_senat == 'ppl11-466'
    assert law.pub_date is None
    assert law.title == u'Proposition de loi tendant à renforcer l\'effectivité de la peine complémentaire d\'interdiction du territoire français et visant à réprimer les délinquants réitérants'


@recorder.use_cassette()
def test_list_pending_law_projects():
    service = LawService()
    laws = service.pending_laws(13, True)

    assert 99 == len(laws)

    assert laws[0].year == 2012
    assert laws[0].legislature == 13
    assert laws[0].type == 'proj'
    assert laws[0].nor is None
    assert laws[0].url_legi == 'https://www.legifrance.gouv.fr/affichLoiPreparation.do?idDocument=JORFDOLE000026052216&type=general&typeLoi=proj&legislature=13'
    assert laws[0].id_legi == 'JORFDOLE000026052216'
    assert laws[0].title == u'Projet de loi ratifiant l’ordonnance n° 2011-1923 du 22 décembre 2011 relative à l\'évolution de la sécurité sociale à Mayotte dans le cadre de la départementalisation'

    assert laws[1].nor == 'DEVA1208027L'


@recorder.use_cassette()
def test_pending_law_project():
    service = LawService()
    law = service.get_law('JORFDOLE000026052216')

    assert law.legislature == 14
    assert law.type == 'proj'
    assert law.kind is None
    assert law.number is None
    assert law.url_an == 'http://www.assemblee-nationale.fr/14/dossiers/ratification_ordonnance_2011-1923.asp'
    assert law.id_an == 'ratification_ordonnance_2011-1923'
    assert law.url_legi == 'https://www.legifrance.gouv.fr/affichLoiPubliee.do?idDocument=JORFDOLE000026052216&type=general'
    assert law.id_legi == 'JORFDOLE000026052216'
    assert law.url_senat == 'http://www.senat.fr/dossier-legislatif/pjl11-607.html'
    assert law.id_senat == 'pjl11-607'
    assert law.pub_date is None
    assert law.title == u'Projet de loi ratifiant l’ordonnance n° 2011-1923 du 22 décembre 2011 relative à l\'évolution de la sécurité sociale à Mayotte dans le cadre de la départementalisation'


@recorder.use_cassette()
def test_list_common_law_projects():
    service = LawService()
    laws = service.common_laws()

    assert 139 == len(laws)

    assert laws[0].common_name == u"loi El Khomri"
    assert laws[0].id_legi == u"JORFTEXT000032983213"
    assert laws[0].nor == u"ETSX1604461L"
    assert laws[0].title == u"LOI n\u00b0 2016-1088 du 8 ao\u00fbt 2016 relative au travail, \u00e0 la modernisation du dialogue social et \u00e0 la s\u00e9curisation des parcours professionnels"
    assert laws[0].url_legi == u"https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000032983213&categorieLien=id"

    assert laws[11].common_name == u"loi ALUR ; loi Duflot"
    assert laws[14].common_name == u"Transposition de l'accord interprofessionnel (ANI) 2013"
    assert laws[17].common_name == u"loi DDADUE ; DADUE"
    assert laws[42].common_name == u"loi TEPA ; paquet fiscal"

    assert laws[-1].common_name == u"loi Marthe Richard"
    assert laws[-1].id_legi == u"JPDF1404194600003138"

