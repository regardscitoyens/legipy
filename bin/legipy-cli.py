#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

import click
import json
import sys

from legipy.services import LawService, LegislatureService


def current_legislature():
    cur = [l for l in LegislatureService.legislatures() if l.end is None]
    return cur[0].number


def _dump_item(obj):
    if obj:
        print(json.dumps(obj.to_json(), sort_keys=True, indent=2))


def _dump_items(ary):
    print(json.dumps([i.to_json() for i in ary], sort_keys=True, indent=2))


@click.group()
def cli():
    pass


@cli.command()
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def published_laws(legislature):
    _dump_items(LawService().published_laws(legislature))


@cli.command()
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def law_projects(legislature):
    _dump_items(LawService().pending_laws(legislature, True))


@cli.command()
@click.option('--legislature', default=current_legislature(),
              help='Legislature number')
def law_proposals(legislature):
    _dump_items(LawService().pending_laws(legislature, False))


@cli.command()
@click.argument('legi_id')
def law(legi_id):
    service = LawService()
    law = service.get_law(legi_id)

    if not law:
        sys.stderr.write('No such law: %s\n' % legi_id)
        exit(1)

    _dump_item(law)


@cli.command()
def legislatures():
    _dump_items(LegislatureService().legislatures())


if __name__ == '__main__':
    cli()
