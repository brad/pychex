"""
This is the heart of the Pychex API. For examples, see :ref:`API-usage`.
"""

import json
import mechanicalsoup
import os
import re
import requests

from lxml import objectify
from tabulate import tabulate

from .exceptions import (
    PychexInvalidPasswordError,
    PychexNoBolUsernameError,
    PychexSecurityImageMismatchError,
    PychexSecurityImageMissingError,
    PychexUnauthenticatedError,
    PychexUnknownError
)

try:
    from collections import OrderedDict
except ImportError:  # Python 2.6 fallback
    from ordereddict import OrderedDict

class PaychexBase(object):
    """ Base class for all classes in the ``paychex`` module. """
    def __init__(self):
        """
        Initialization prepares a ``mechanicalsoup.Browser`` object with the
        right presets and sets up some commond member variables.
        """
        self.benefits_url = 'https://benefits.paychex.com'
        self.browser = mechanicalsoup.Browser()
        # Use an HTTPAdapter with max_retries set to 3 because sometimes
        # the calls throw ConnectionError exceptions for no apparent reason
        self.adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.browser.session.mount('https://', self.adapter)
        self.text_html = {'content-type': 'text/html; charset=utf-8'}
        self.browser.session.headers.update(self.text_html)
        self.logged_in = False

class Paychex(PaychexBase):
    """
    The Paychex class provides the ability to login to https://mypaychex.com
    and retrieve the Benefits OnLine username.
    """
    def __init__(self, username, security_image_path=None):
        """
        Initialization sets up member variables with the needed URLs and empty
        variables for credentials.

        Arguments:

        * *username* -- The username for logging in to https://mypaychex.com

        Keyword arguments:

        * *security_image_path* -- The security image path obtained and saved
          from a previous login. Makes it possible to skip a couple steps in
          the flow (optional).
        """
        super(Paychex, self).__init__()
        self.start_url = 'https://www.mypaychex.com'
        self.base_url = 'https://landing.paychex.com'
        self.login_url = '%s/ssologin/Login.aspx' % self.base_url
        # Set up other member variables
        self.username = username
        self.security_image_path = security_image_path
        self.password = None

    def post_username(self):
        """
        Post the username and save the security image. It is up to the client
        to verify this is the corrert security image before proceeding. If
        ``security_image_path`` was supplied during initialization, it will be
        verified here.

        Raises:

        * *PychexSecurityImageMismatchError* -- If the supplied
          ``security_image_path`` doesn't match what is returned from Paychex
        """

        self.login_page = self.browser.get(self.start_url, verify=True)
        self.browser.session.headers.update(
            {'content-type': 'application/json; charset=utf-8'})
        data = json.dumps({'enteredUsername': self.username})
        res = self.browser.post('%s/GetSecurityImage' % self.login_url,
                                data=data)
        security_image_path = res.json()['d']
        if not self.security_image_path:
            self.security_image_path = security_image_path
        elif self.security_image_path != security_image_path:
            raise PychexSecurityImageMismatchError(
                'The security image did not match')

    def get_security_image(self):
        """
        Returns the absolute url of the security image.

        Raises:

        * *PychexSecurityImageMissingError* -- If we don't have an image yet
        """

        if self.security_image_path:
            return '%s%s' % (self.base_url, self.security_image_path)
        else:
            raise PychexSecurityImageMissingError(
                'You must call post_username before get_security_image')

    def login(self, password):
        """
        Login to Paychex using the username supplied previously, along with
        the password supplied as an argument.

        Arguments:

        * *password* -- The password for https://mypaychex.com

        Raises:

        * *PychexSecurityImageMissingError* -- If we don't have an image yet
        * *PychexInvalidPasswordError* -- If the password supplied is invalid

        Returns:

        * *bool* -- Whether login succeed or not
        """

        if not self.security_image_path:
            raise PychexSecurityImageMissingError(
                'Before providing the password, please post the username '
                'and verify the security image')

        self.password = password
        data = json.dumps({'eu': self.username, 'ep': self.password})
        res = self.browser.post("%s/ProcessLogin" % self.login_url, data=data)

        # Submit the login form
        form = self.login_page.soup.select('#Serverform')[0]
        form.select('#USER')[0]['value'] = self.username
        form.select('#PASSWORD')[0]['value'] = self.password
        form.select('#target')[0]['value'] = res.json()['d']
        self.browser.session.headers.update(self.text_html)
        res = self.browser.submit(
            form, '%s/ssologin/' % self.base_url)
        self.logged_in = len(res.soup.select('#Error_Login .Error')) == 0
        if not self.logged_in:
            raise PychexInvalidPasswordError(
                'The login information you entered does not match our '
                'records. Accounts will lock after 5 failed attempts to log '
                'on.')
        return True

    def get_bol_username(self):
        """
        Get the Benefits OnLine app username via a SOAP request

        Raises:

        * *PychexUnauthenticatedError* -- If you haven't logged in yet
        * *PychexNoBolUsernameError* -- If there was no Benefits OnLine
          username in the XML returned from the API. This usually means that
          there is no Retirement account associated with the Paychex account.

        Returns:

        * *string* -- The Benefits OnLine username for use with the
          ``BenefitsOnline`` class
        """

        if not self.logged_in:
            raise PychexUnauthenticatedError(
                'You must login before calling get_bol_username')

        soap_content = open(os.path.join(
            os.path.dirname(__file__), 'templates',
            'GetUserApplicationAccountData.soap.xml')).read()
        data = soap_content.format(username=self.username)
        service = 'OneSourceService.asmx'
        soap_action = '%s/GetUserApplicationAccountData' % service
        res = self.browser.post(
            '%s/%s' % (self.base_url, service), data=data, headers={
                'Referer': 'Pychex',
                'Content-Type': 'text/xml; charset=utf-8',
                'Content-Length': len(data),
                'SOAPAction': soap_action,
            })
        xml_obj = objectify.fromstring(res.content)
        key1 = '{%s}GetUserApplicationAccountDataResponse' % service
        key2 = '{%s}GetUserApplicationAccountDataResult' % service
        key3 = '{%s}LinkedAccounts' % service
        accounts = xml_obj.Body[key1][key2][key3].getchildren()
        for account in accounts:
            if account['{%s}AppId' % service] == 'BOL':
                return account['{%s}ClientId' % service].text
        raise PychexNoBolUsernameError(
            'Unable to retrieve Benefits OnLine app username')


class BenefitsOnline(PaychexBase):
    """ Used to login to the Paychex Benefits OnLine app. """
    def __init__(self, bol_username, password):
        """
        Initialization sets up member variables containing credentials, and an
        empty variable to use for the ``RetirementServices`` object when we get
        it.

        Arguments:

        * *bol_username* -- The Benefits OnLine username obtained from
          ``Pychex.get_bol_username``
        * *password* -- The same password used to log in to
          https://mypaychex.com
        """
        super(BenefitsOnline, self).__init__()
        self.bol_username = bol_username
        self.password = password
        self.retirement_services = None

    def login(self):
        """
        Login to the Benefits Online portal using the credentials saved to
        member variables. If the login is successful, the
        ``retirement_services`` member variable will be populated with a
        ``RetirementServices`` object supplied with the current session, ready
        to login.

        Raises:

        * *PychexInvalidPasswordError* -- If you supplied the wrong password

        Returns:

        * *bool* -- Whether the login was successful or not
        """
        # SSOLogin
        res = self.browser.post(
            '%s/cgi-bin/contactus_es/ssologin_es' % self.benefits_url, data={
                'AppPass': self.password,
                'AppUsername': self.bol_username
            })
        # Standard Login
        std_login_form = 'form[name="PaychexStdLogin"]'
        form = res.soup.select(std_login_form)[0]
        form['action'] = '%s/smlogin/login.fcc' % self.benefits_url
        res = self.browser.submit(form)
        self.logged_in = len(res.soup.select(std_login_form)) == 0
        if not self.logged_in:
            raise PychexInvalidPasswordError(
                'The login information you entered does not match our '
                'records. Accounts will lock after 5 failed attempts to log '
                'on.')
        self.retirement_services = RetirementServices(self.browser)
        return True


class RetirementServices(PaychexBase):
    """
    A class that provides read-only access to the Paychex Retirement
    Services app.
    """
    def __init__(self, browser):
        """
        Initialization sets up empty member variables and overrides the
        ``browser`` member variable with the one passed in as an argument.

        Member variables:

        * *current_balance* -- The user's current balance
        * *vested_balance* -- The user's vested balance
        * *personal_ror* -- The user's personal rate of return
        * *balance_tab_info* -- The same information that is shown in the
          balance tab of Retirement Services, stored in a dictionary. An
          example of this can be seen in :ref:`CLI-usage`.

        Arguments:

        * *browser* -- A ``mechanicalsoup.Browser`` object. This ``Browser``
          should be the same one that logged in to Benefits OnLine. This primes
          it for login to Retirement Services
        """
        super(RetirementServices, self).__init__()
        self.browser = browser
        self.current_balance = None
        self.vested_balance = None
        self.personal_ror = None
        self.balance_tab_info = None

    def login(self):
        """
        Login to the retirement services app

        Raises:

        * *PychexUnknownError* -- In all my testing of this method, I never
          managed to reproduce an error. However, if the response doesn't have
          a status code of 200, this exception will be raised.

        Returns:

        * *bool* -- Whether the login was successful or not
        """

        res = self.browser.get('%s/cgi-bin/401k/401kstart' % self.benefits_url)
        form = res.soup.select('form[name="PaychexSSNLogin"]')[0]
        form['action'] = '%s/401k_emp/do/LoginForm' % self.benefits_url
        res = self.browser.submit(form)
        # I was unable to get this form submission to fail, even when I change
        # the username and SSN (in that case it still knows who I am and
        # retrieves my data only). The form still needs to be submitted, and
        # logged_in will only be False if the status code is not 200
        self.logged_in = res.status_code == 200
        if not self.logged_in:
            raise PychexUnknownError('An unknown error occurred, please try '
                                     'again later: %s' % res.content)
        return True

    def get_account_summary(self):
        """
        Get the 401k account summary. The Paychex Retirement Services app has
        many endpoints that respond with small snippets of HTML. This method
        hits a couple of them and saves the account summary information to the
        ``current_balance``, ``vested_balance``, ``personal_ror``, and
        ``balance_tab_info`` member variables.

        Raises:

        * *PychexUnauthenticatedError* -- If you haven't logged in to
          Retirement Services yet

        Returns:

        * *bool* -- Whether the method succeeded or not
        """

        if not self.logged_in:
            raise PychexUnauthenticatedError(
                'You must login before calling get_account_summary')

        # Get the account summary
        res = self.browser.get(
            '%s/401k_emp/xhr/accountSummary' % self.benefits_url)
        welcomeBoxData = res.soup.select('div.welcomeBoxData')
        self.current_balance = welcomeBoxData[0].text
        self.vested_balance = welcomeBoxData[1].text
        self.personal_ror = res.soup.select('div.welcomeBoxRorData')[0].text

        # Get the balance tab data
        res = self.browser.get(
            '%s/401k_emp/do/xhr/getBalanceTab' % self.benefits_url)
        return self.parse_balance_tab_data(res)

    def parse_balance_tab_data(self, res):
        """
        Parse out the balance tab information from the HTML in the given
        response.

        Arguments:

        * *res* -- A response obj from a call to the Retirement Services
          ``accountSummary`` endpoint

        Returns:

        * *bool* -- Whether the method succeeded or not
        """

        funds = res.soup.select('#balanceByFundTable tr')
        self.balance_tab_info = {}
        cls = ['percent', 'symbol', 'fund', 'shares', 'balance', 'prospectus']
        for fund in funds:
            cells = fund.select('td')
            fund_dict = {}
            symbol = None
            for i, cell_title in enumerate(cls):
                if cell_title == 'fund':
                    link = cells[i].select('a')
                    onclick = link[0]['onclick']
                    search = re.search(r"window.open\('(.*)'\)", onclick)
                    fund_dict[cell_title] = {
                        'name': link[0].text.strip(),
                        'url': search.groups()[0].replace('&amp;', '&')
                    }
                elif cell_title == 'prospectus':
                    element = cells[i].select('acronym img')[0]
                    onclick = element['onclick']
                    search = re.search(r"window.open\('(.*)'\)", onclick)
                    cell_text = search.groups()[0]
                    fund_dict[cell_title] = cell_text.replace('&amp;', '&')
                else:
                    cell_text = cells[i].text.strip()
                    if cell_title == 'symbol':
                        symbol = cell_text
                    fund_dict[cell_title] = cell_text
            self.balance_tab_info[symbol] = fund_dict
        return True

    def formatted_summary(self):
        """
        Format the summary in a more printable manner. This is the format
        presented by the CLI, as shown in :ref:`CLI-usage`.

        Returns:

        * *string* -- A formatted table of investment balance information,
          bearing a striking resemblence to the table in the balance tab of
          the Paychex Retirement Services app
        """

        balances = [v for (k, v) in self.balance_tab_info.items()]
        if len(balances) == 0:
            return ''
        urls = []
        ordered_balances = []
        ordered_keys = ['percent', 'symbol', 'fund', 'shares', 'balance',
                        'prospectus']
        symbol_sort = lambda balance: balance['symbol']
        for i, balance in enumerate(sorted(balances, key=symbol_sort)):
            urls.append(balance['fund']['url'])
            balance['fund'] = '%s [%i]' % (balance['fund']['name'], len(urls))
            urls.append(balance['prospectus'])
            balance['prospectus'] = '[%i]' % len(urls)
            ordered_balances.append(OrderedDict([
                (key, balance[key]) for key in ordered_keys]))

        return '%s\n\n%s' % (
            tabulate(ordered_balances, headers='keys'),
            '\n'.join(['[%i] %s' % (i+1, url) for i, url in enumerate(urls)]))
