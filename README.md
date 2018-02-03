legipy
======

[![Build Status](https://travis-ci.org/regardscitoyens/legipy.svg?branch=master)](https://travis-ci.org/regardscitoyens/legipy)
[![codecov](https://codecov.io/gh/regardscitoyens/legipy/branch/master/graph/badge.svg)](https://codecov.io/gh/regardscitoyens/legipy)

Python client for the `legifrance.gouv.fr` website.

CLI usage
---------

The command-line script `legipy` gives access to service commands from the command line and outputs data in JSON format.

### List legislatures

`legipy legislatures`

### List published laws

`legipy published_laws [--legislature=CURRENT]`

### List pending law projects

`legipy law_projects [--legislature=CURRENT]`

### List pending law proposals

`legipy law_proposals [--legislature=CURRENT]`

### List common laws ("[Lois dites](https://www.legifrance.gouv.fr/affichSarde.do?reprise=true&page=1&idSarde=SARDOBJT000007106573)")

`legipy-cli.py common_laws`

### Show specific law

`legipy law JORFDOLE000024106525`
