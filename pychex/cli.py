"""Pychex command-line interface

Usage:
  pychex authorize <username> [--config=<config_file>]
  pychex account_summary [--config=<config_file>]

Options:
  -h --help               Show this screen.
  --version               Show version.
  --config=<config_file>  The config file to use [default: ./pychex.cfg]
"""
from __future__ import absolute_import

import getpass
import requests

from base64 import b64decode, b64encode
from docopt import docopt
from PIL import Image
from tabulate import tabulate

from . import __version__
from .paychex import Paychex

try:
    import configparser
    from io import BytesIO
except ImportError:  # Python 2.x fallback
    import ConfigParser as configparser
    from StringIO import StringIO as BytesIO

try:
    input = raw_input
except NameError:  # Python > 3.1 has no raw_input
    pass

try:
    from collections import OrderedDict
except ImportError:  # Python 2.6 fallback
    from ordereddict import OrderedDict


class PychexCli:
    def __init__(self, arguments):
        self.config_file = arguments['--config']
        self.config = configparser.ConfigParser()

        if arguments['authorize']:
            self.authorize(arguments)
        elif arguments['account_summary']:
            try:
                self.read_config()
            except (configparser.NoOptionError, configparser.NoSectionError,
                    IOError):
                print('Error reading credentials, please run: '
                      'pychex authenticate <username>')
            else:
                self.get_account_summary()

    def get_input(self, text):
        return input(text).lower()

    def read_config(self):
        with open(self.config_file) as cfg:
            self.config.readfp(cfg)
        self.username = self.b64decode(self.config.get('pychex', 'username'))
        self.security_image_path = self.b64decode(self.config.get(
            'pychex', 'security_image_path'))
        self.password = self.b64decode(self.config.get('pychex', 'password'))

    def write_config(self, security_image_path, password):
        self.config.add_section('pychex')
        self.config.set('pychex', 'username', self.b64encode(self.username))
        self.config.set('pychex', 'security_image_path',
                        self.b64encode(security_image_path))
        self.config.set('pychex', 'password', self.b64encode(password))
        with open(self.config_file, 'w') as cfg:
            self.config.write(cfg)

    def authorize(self, arguments):
        self.username = arguments['<username>']
        paychex = Paychex(self.username)
        paychex.post_username()
        img_dat = requests.get(paychex.get_security_image()).content
        Image.open(BytesIO(img_dat)).show()
        choice = self.get_input('Is this your security image (Y/n)? ')
        # input returns the empty string for "enter"
        chose_yes = choice in set(['yes', 'y', 'ye', ''])
        chose_no = choice in set(['no', 'n'])
        if chose_no:
            print('Security image mismatch.')
        elif not chose_yes:
            print('Please respond with "yes" or "no".')
        else:
            # Get the password and write the credentials to a file
            password = getpass.getpass('Password (input hidden): ')
            self.write_config(paychex.security_image_path, password)
            print('Credentials written to %s' % self.config_file)

    def get_account_summary(self):
        paychex = Paychex(self.username, self.security_image_path)
        # This step automatically verifies the security image
        paychex.post_username()
        paychex.login(self.password)
        paychex.get_account_summary()

        print('Current balance: %s' % paychex.current_balance)
        print('Vested balance: %s' % paychex.vested_balance)
        print('Personal RoR: %s\n' % paychex.personal_ror)

        # Reformat the information in a way that is more palatable to tabulate
        balances = [v for (k, v) in paychex.balance_tab_info.items()]
        if len(balances):
            urls = []
            ordered_balances = []
            ordered_keys = ['percent', 'symbol', 'fund', 'shares', 'balance',
                            'prospectus']
            symbol_sort = lambda balance: balance['symbol']
            for i, balance in enumerate(sorted(balances, key=symbol_sort)):
                urls.append(balance['fund']['url'])
                balance['fund'] = '%s [%i]' % (balance['fund']['name'],
                                               len(urls))
                urls.append(balance['prospectus'])
                balance['prospectus'] = '[%i]' % len(urls)
                ordered_balances.append(OrderedDict([
                    (key, balance[key]) for key in ordered_keys]))

            print(tabulate(ordered_balances, headers='keys'))
            print('')
            for i, url in enumerate(urls):
                print('[%i] %s' % (i+1, url))

    def b64encode(self, str_):
        return b64encode(str_.encode('utf8')).decode('utf8')

    def b64decode(self, str_):
        return b64decode(str_.encode('utf8')).decode('utf8')


def main():
    arguments = docopt(__doc__, version='Pychex %s' % __version__)
    PychexCli(arguments)

if __name__ == '__main__':
    main()
