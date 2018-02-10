#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

import datetime
import json
import sys

import click

from legipy.models.base import LegipyModel
from legipy.services.code_service import CodeService
from legipy.services.code_service import SectionService
from legipy.services.law_service import LawService
from legipy.services.legislature_service import LegislatureService


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, LegipyModel):
        return obj.to_json()
    elif isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError("Type {0} not serializable".format(repr(type(obj))))


def current_legislature():
    cur = [l for l in LegislatureService.legislatures() if l.end is None]
    return cur[0].number


@click.group(short_help=u"Client for the `legifrance.gouv.fr` website.")
def cli():
    pass


@cli.command(short_help=u"List published laws")
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def published_laws(legislature):
    obj = LawService().published_laws(legislature)
    print(json.dumps(obj, indent=2, default=json_serial))


@cli.command(short_help=u"List pending law projects")
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def law_projects(legislature):
    obj = LawService().pending_laws(legislature, True)
    print(json.dumps(obj, indent=2, default=json_serial))


@cli.command(short_help=u"List pending law proposals")
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def law_proposals(legislature):
    obj = LawService().pending_laws(legislature, False)
    print(json.dumps(obj, indent=2, default=json_serial))


@cli.command(short_help=u"Show specific law")
@click.argument('legi_id')
def law(legi_id):
    obj = LawService().get_law(legi_id)
    if not obj:
        sys.stderr.write('No such law: %s\n' % legi_id)
        exit(1)
    print(json.dumps(obj, indent=2, default=json_serial))


@cli.command(short_help=u"List legislatures")
def legislatures():
    obj = LegislatureService().legislatures()
    print(json.dumps(obj, indent=2, default=json_serial))


@cli.command(short_help=u"List applicable codes")
def codes():
    obj = CodeService().codes()
    print(json.dumps(obj, indent=2, default=json_serial))


@cli.command(short_help=u"Show code detail")
@click.argument('id-code')
@click.option('--date-pub', help=u"Publication date (ISO format), default to today")
@click.option('--with-articles/--without-articles', default=False, help=u"Show details for each articles")
def code(id_code, date_pub, with_articles):
    if date_pub:
        date_pub = date_pub.replace('-', '')  # 2018-02-01  => 20180201
    obj = CodeService().code(id_code, date_pub, with_articles)
    print(json.dumps(obj, indent=2, default=json_serial))


@cli.command(short_help=u"Show code detail")
@click.argument('id-code')
@click.argument('id-section')
@click.option('--date-pub', help=u"Publication date (ISO format), default to today")
def code_section(id_code, id_section, date_pub):
    obj = SectionService().articles(id_code, id_section, date_pub)
    print(json.dumps(obj, indent=2, default=json_serial))


if __name__ == '__main__':
    cli()
