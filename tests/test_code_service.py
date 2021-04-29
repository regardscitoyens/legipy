# coding: utf-8
import datetime

import vcr

from legipy.models.code import Article
from legipy.models.code import Code
from legipy.services.code_service import CodeService
from legipy.services.code_service import SectionService

recorder = vcr.VCR(cassette_library_dir='tests/fixtures/cassettes')


@recorder.use_cassette()
def test_code_service__codes():
    service = CodeService()
    codes = service.codes()  # type: list

    # 74 en vigueur + 1 en vigueur différée (> 30/9/2021) + 30 abrogés
    assert len(codes) == 105

    code = codes[0]
    assert isinstance(code, Code)
    assert code.id_code == u'LEGITEXT000006074069'
    assert code.title == u"Code de l'action sociale et des familles"
    assert code.subtitle is None
    assert code.date_pub is None
    assert code.url_code == u'https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006074069'
    assert code.children is None

    code = codes[1]
    assert isinstance(code, Code)
    assert code.id_code == u'LEGITEXT000006075116'
    assert code.title == u"Code de l'artisanat"
    assert code.subtitle is None
    assert code.date_pub is None
    assert code.url_code == u'https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006075116'
    assert code.children is None


@recorder.use_cassette()
def test_code_service__code():
    service = CodeService()
    id_code = u'LEGITEXT000006074069'
    code = service.code(id_code, date_pub='2018-02-11', with_articles=False)

    assert isinstance(code, Code)
    assert code.id_code == id_code
    assert code.title == u"Code de l'action sociale et des familles"
    assert code.subtitle == u"Version en vigueur au 11 février 2018"
    assert code.date_pub == datetime.date(2018, 2, 11)
    assert code.url_code == (u"https://www.legifrance.gouv.fr/codes"
                             u"/texte_lc/LEGITEXT000006074069/2018-02-11/")
    assert code.children is not None
    assert len(code.children) == 3

    expected_list = [
        {
            'id_section': u'LEGISCTA000006107980',
            'title': u'Partie législative'
        },
        {
            'id_section': u'LEGISCTA000006112899',
            'title': u'Partie réglementaire'
        },
        {
            'id_section': u'LEGISCTA000018780362',
            'title': u'Annexe',
            'articles': u'Articles Annexe 1-1 à Annexe 4-10',
            'url_section': (u'https://www.legifrance.gouv.fr/codes/section_lc'
                            u'/LEGITEXT000006074069/LEGISCTA000018780362'
                            u'/2018-02-11/')
        }]
    for child, expected in zip(code.children, expected_list):
        for key, value in expected.items():
            assert getattr(child, key) == value


@recorder.use_cassette()
def test_section_service__articles():
    service = SectionService()
    id_code = u'LEGITEXT000006074069'
    id_section = u'LEGISCTA000018780362'
    articles = service.articles(id_code, id_section, date_pub='2018-02-11')

    assert len(articles) == 43
    article = articles[0]
    assert isinstance(article, Article)
    assert article.title == u"Annexe 1-1"
    assert article.history == (u"Modifié par "
            u"Ordonnance n°2016-301 du 14 mars 2016 - art. 2 (V)")
