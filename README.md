legipy
======

[![Build Status](https://travis-ci.org/regardscitoyens/legipy.svg?branch=master)](https://travis-ci.org/regardscitoyens/legipy)
[![codecov.io](https://codecov.io/github/regardscitoyens/legipy/coverage.svg?branch=master)](https://codecov.io/github/regardscitoyens/legipy?branch=master)

Python client for the `legifrance.gouv.fr` website.

CLI usage
---------

The command-line script `legipy-cli.py` gives access to service commands from the command line and outputs data in JSON format.

### List published laws

`legipy-cli.py published_laws [--legislature=14]`

### List pending law projects

`legipy-cli.py law_projects [--legislature=14]`

### List pending law proposals

`legipy-cli.py law_proposals [--legislature=14]`

### Show specific law

`legipy-cli.py law JORFDOLE000024106525`