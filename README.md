legipy
======

[![Build Status](https://travis-ci.org/regardscitoyens/legipy.svg?branch=master)](https://travis-ci.org/regardscitoyens/legipy)
[![codecov](https://codecov.io/gh/regardscitoyens/legipy/branch/master/graph/badge.svg)](https://codecov.io/gh/regardscitoyens/legipy)

Python client for the `legifrance.gouv.fr` website.

CLI usage
---------

The command-line script `legipy` gives access to service commands from the command line and outputs data in JSON format.

## Legislature

Access to the [legislature](https://www.legifrance.gouv.fr/dossiers_legislatifs.jsp).

### List legislatures

```bash
legipy legislatures
```

### List published laws

```bash
legipy published_laws [--legislature=CURRENT]
```

### List pending law projects

```bash
legipy law_projects [--legislature=CURRENT]
```

### List pending law proposals

```bash
legipy law_proposals [--legislature=CURRENT]
```

### List common laws ("[Lois dites](https://www.legifrance.gouv.fr/affichSarde.do?reprise=true&page=1&idSarde=SARDOBJT000007106573)")

```bash
legipy common_laws
```

### Show specific law

```bash
legipy law JORFDOLE000024106525
```

## Applicable codes

Access to the [applicable codes](https://www.legifrance.gouv.fr/initRechCodeArticle.do).

### List applicable codes

```bash
legipy codes
```

### Show code details

```bash
legipy code LEGITEXT000006074075
legipy code --date-pub 2018-05-01 LEGITEXT000006074075
```

### Show code section details

```bash
legipy code_section LEGITEXT000006074075 LEGISCTA000006107991
legipy code --date-pub 2018-05-01 LEGITEXT000006074075 LEGISCTA000006107991
```
