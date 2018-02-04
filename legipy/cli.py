#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

import json
import sys

import click

from legipy.services import LawService, LegislatureService
from legipy.services.code_service import CodeService


def current_legislature():
    cur = [l for l in LegislatureService.legislatures() if l.end is None]
    return cur[0].number


def _dump_item(obj):
    if obj:
        print(json.dumps(obj.to_json(), sort_keys=True, indent=2))


def _dump_items(ary):
    print(json.dumps([i.to_json() for i in ary], sort_keys=True, indent=2))


@click.group()
def cli(short_help="Client for the `legifrance.gouv.fr` website."):
    pass


@cli.command(short_help="List published laws")
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def published_laws(legislature):
    _dump_items(LawService().published_laws(legislature))


@cli.command(short_help="List pending law projects")
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def law_projects(legislature):
    _dump_items(LawService().pending_laws(legislature, True))


@cli.command(short_help="List pending law proposals")
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def law_proposals(legislature):
    _dump_items(LawService().pending_laws(legislature, False))


@cli.command("List common law (« lois dites »)")
def common_laws():
    _dump_items(LawService().common_laws())


@cli.command(short_help="Show specific law")
@click.argument('legi_id')
def law(legi_id):
    service = LawService()
    law = service.get_law(legi_id)

    if not law:
        sys.stderr.write('No such law: %s\n' % legi_id)
        exit(1)

    _dump_item(law)


@cli.command(short_help="List legislatures")
def legislatures():
    _dump_items(LegislatureService().legislatures())


@cli.command(short_help="Recherche simple dans les codes en vigueur")
def codes():
    _dump_items(CodeService().codes())


@cli.command(short_help="Détail d'un code")
@click.argument('id-code')
@click.option('--date-pub', help=u"Publication date (ISO format), default to today")
def code(id_code, date_pub):
    if date_pub:
        date_pub = date_pub.replace('-', '')  # 2018-02-01  => 20180201
    _dump_item(CodeService().code(id_code, date_pub))


if __name__ == '__main__':
    cli()
