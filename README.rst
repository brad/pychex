Pychex
=============

.. image:: https://circleci.com/gh/brad/pychex.png?style=shield
    :target: https://circleci.com/gh/brad/pychex

.. image:: https://requires.io/github/brad/pychex/requirements.svg?branch=master
     :target: https://requires.io/github/brad/pychex/requirements/?branch=master
     :alt: Requirements Status

Paychex Benefits OnLine access library

Install with `pip install pychex`

Quick start
======

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

* Python 2.7
