Pychex
======

.. image:: https://travis-ci.org/brad/pychex.svg?branch=master
   :target: https://travis-ci.org/brad/pychex

.. image:: https://coveralls.io/repos/brad/pychex/badge.png?branch=master
   :target: https://coveralls.io/r/brad/pychex?branch=master

.. image:: https://requires.io/github/brad/pychex/requirements.svg?branch=master
   :target: https://requires.io/github/brad/pychex/requirements/?branch=master
   :alt: Requirements Status

Paychex Benefits OnLine access library and client

This library and command line client can be used to authorize and retrieve the
account summary data from Paychex Benefits OnLine. Note that this is only for
those who login using https://mypaychex.com. If you login to Paychex via
https://paychexonline.com this application will not currently work, but with
your help we should be able to support it as well.

Requirements
============

* Python >= 2.6, Python >= 3.x, or PyPy. You can download it from `here <https://www.python.org/>`_
* Pip. If you have Python >= 2.7.9 or >= 3.4 then you already have ``pip``. Otherwise, please follow `these instructions <https://pip.pypa.io/en/latest/installing.html>`_

Install
=======

Once you have satisfied the requirements listed above, install by running the
following command from the
`terminal <http://cli.learncodethehardway.org/book/ex1.html>`_: ::

    pip install pychex

Quick start
===========

After installing you will have use of a command line ``pychex`` client
application. Run ``pychex authorize <username>`` to confirm your security
image and login. This will save your encrypted credentials to a
``pychex.cfg`` file. NOTE: The encryption does very little to protect your
credentials from a determined and malicious intruder, and the ultimate
responsibility in protecting your credentials is yours. After you have
authorized the client, you can get a printout of your account summary by
running ``pychex account_summary``. Full usage instructions below: ::

    Pychex command-line interface

    Usage:
      pychex authorize <username> [--config=<config_file>]
      pychex account_summary [--config=<config_file>]

    Options:
      -h --help               Show this screen.
      --version               Show version.
      --config=<config_file>  The config file to use [default: ./pychex.cfg]

Running ``pychex account_summary`` will result in output similar to the
following fake data: ::

    Current balance: $67,872.49
    Vested balance: $67,872.49
    Personal RoR: 8.9%

      percent  symbol    fund               shares  balance     prospectus
    ---------  --------  ---------------  --------  ----------  ------------
         9.79  FNAMW     FAKE NAME W [1]   103.572  $6,644.72   [2]
        10.21  FNAMX     FAKE NAME X [3]   214.321  $6,929.78   [4]
        31.58  FNAMY     FAKE NAME Y [5]    13.179  $21,434.13  [6]
        48.42  FNAMZ     FAKE NAME Z [7]    26.624  $32,863.86  [8]

    [1] http://www.example.com/?product=FUNDS&custno=1&FUNDID=1
    [2] http://www.example.com/?product=PROSP&custno=1&FUNDID=1
    [3] http://www.example.com/?product=FUNDS&custno=1&FUNDID=2
    [4] http://www.example.com/?product=PROSP&custno=1&FUNDID=2
    [5] http://www.example.com/?product=FUNDS&custno=1&FUNDID=3
    [6] http://www.example.com/?product=PROSP&custno=1&FUNDID=3
    [7] http://www.example.com/?product=FUNDS&custno=1&FUNDID=4
    [8] http://www.example.com/?product=PROSP&custno=1&FUNDID=4

Slow start
==========

And here are some examples for how to use it programmatically: ::

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

Development
===========

You can also use the CLI from a git checkout. First, install all the
dependencies by running ``pip install -r requirements/dev.txt``. Then you can run
the CLI like so: ::

    $ python -m pychex.cli <args>

You can run the tests simply by running the ``behave`` command
