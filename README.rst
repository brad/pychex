Pychex
=============

.. image:: https://travis-ci.org/brad/pychex.svg?branch=master
    :target: https://travis-ci.org/brad/pychex

.. image:: https://coveralls.io/repos/brad/pychex/badge.png?branch=master
    :target: https://coveralls.io/r/brad/pychex?branch=master

.. image:: https://requires.io/github/brad/pychex/requirements.svg?branch=master
     :target: https://requires.io/github/brad/pychex/requirements/?branch=master
     :alt: Requirements Status

Paychex Benefits OnLine access library

Install with `pip install pychex`

Quick start
===========

After installing you will have use of a command line `pychex` client
application. Run `pychex authorize <username>` to confirm your security
image and login. This will save your encrypted credentials to a
`pychex.cfg` file. NOTE: The encryption does very little to protect your
credentials from a determined and malicious intruder, and the ultimate
responsibility in protecting your credentials is yours. After you have
authorized the client, you can get a printout of your account summary by
running `pychex account_summary`. Full usage instructions below: ::
    Pychex command-line interface

    Usage:
      pychex authorize <username> [--config=<config_file>]
      pychex account_summary [--config=<config_file>]

    Options:
      -h --help               Show this screen.
      --version               Show version.
      --config=<config_file>  The config file to use [default: ./pychex.cfg]

Slow start
==========
::
    >>> from pychex import Paychex
    >>> paychex = Paychex(username)
    >>> paychex.post_username()
    >>> paychex.get_security_image()
    u'https://landing.paychex.com/ssologin/Media/Images/Security/Butterfly.gif'
    >>> paychex.login(password)
    True
    >>> paychex.get_account_summary()
    True
    >>> paychex.current_balance
    '$XX,XXX.XX'
    >>> paychex.vested_balance
    '$XX,XXX.XX'
    >>> paychex.personal_ror
    'X.XX%'
    >>> for symbol, row in paychex.balance_tab_info.items():
    ...     for label, cell in row.items():
    ...         print('%s: %s' % (label, cell))
    ...
    symbol: XXXX1
    percent: XX.XX
    shares: XXX.XXX
    fund: {'url': 'http://www.sponsorportal.com/content/content.cfm?product=FUNDS&custno=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXXXX&FUNDID=XXXXXXXXX&cusip=XXXXXXXXX', 'name': 'XXXX XXXXXXX1'}
    balance: $X,XXX.XX
    prospectus: http://www.sponsorportal.com/content/content.cfm?product=PROSP&custno=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXXXX&FUNDID=XXXXXXXXX&cusip=XXXXXXXXX]
    symbol: XXXX2
    percent: XX.XX
    shares: XXX.XXXX
    fund: {'url': 'http://www.sponsorportal.com/content/content.cfm?product=FUNDS&custno=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXXXX&FUNDID=XXXXXXXXX&cusip=XXXXXXXXX', 'name': 'XXXX XXXXXXX2'}
    balance: $XX,XXX.XX
    prospectus: http://www.sponsorportal.com/content/content.cfm?product=PROSP&custno=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXXXX&FUNDID=XXXXXXXXX&cusip=XXXXXXXXX


Requirements
============

* Python 2.6+ (including Python 3.x) or PyPy
