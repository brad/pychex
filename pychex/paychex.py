"""
This file contains the Paychex class. For detailed documentation on how to use
the class, see the README.
"""

import json
import mechanicalsoup
import os
import re
import requests

from lxml import objectify

from .exceptions import (
    PychexInvalidPasswordError,
    PychexNoAppUsernameError,
    PychexSecurityImageMismatchError,
    PychexSecurityImageMissingError,
    PychexUnauthenticatedError
)


class Paychex:
    """
    This class provides login and basic read-only communication with the
    Paychex Benefits OnLine portal
    """

    def __init__(self, username, security_image_path=None):
        self.start_url = 'https://www.mypaychex.com'
        self.base_url = 'https://landing.paychex.com'
        self.login_url = '%s/ssologin/Login.aspx' % self.base_url
        self.benefits_url = 'https://benefits.paychex.com'
        # Prepare the session
        self.app_json = {'content-type': 'application/json; charset=utf-8'}
        self.text_html = {'content-type': 'text/html; charset=utf-8'}
        self.browser = mechanicalsoup.Browser()
        # Use an HTTPAdapter with max_retries set to 3 because sometimes
        # the calls throw ConnectionError exceptions for no apparent reason
        self.adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.browser.session.mount('https://', self.adapter)
        self.browser.session.headers.update(self.text_html)
        # Set up other member variables
        self.logged_in = False
        self.app_username = None
        self.common_data = {'USER': username}
        self.security_image_path = security_image_path
        self.current_balance = None
        self.vested_balance = None
        self.personal_ror = None
        self.balance_tab_info = None

    def post_username(self):
        """
        Post the username and save the security image. It is up to the
        client to verify this is the corrert security image before proceeding
        """

        # No need to verify the certificate on this page as it's not where we
        # post the username/password
        requests.packages.urllib3.disable_warnings()
        self.login_page = self.browser.get(self.start_url, verify=False)
        self.browser.session.headers.update(self.app_json)
        data = json.dumps({'enteredUsername': self.common_data['USER']})
        res = self.browser.post('%s/GetSecurityImage' % self.login_url,
                                data=data)
        security_image_path = res.json()['d']
        if not self.security_image_path:
            self.security_image_path = security_image_path
        elif self.security_image_path != security_image_path:
            raise PychexSecurityImageMismatchError(
                'The security image did not match')

    def get_security_image(self):
        """  Returns the absolute url of the security image  """

        if self.security_image_path:
            return '%s%s' % (self.base_url, self.security_image_path)
        else:
            raise PychexSecurityImageMissingError(
                'You must call post_username before get_security_image')

    def login(self, password):
        """ Login to Paychex """

        if not self.security_image_path:
            raise PychexSecurityImageMissingError(
                'Before providing the password, please post the username '
                'and verify the security image')

        self.common_data['PASSWORD'] = password
        data = json.dumps({
            'eu': self.common_data['USER'],
            'ep': self.common_data['PASSWORD']
        })
        res = self.browser.post("%s/ProcessLogin" % self.login_url, data=data)

        # Submit the login form
        form = self.login_page.soup.select('#Serverform')[0]
        form.select('#USER')[0]['value'] = self.common_data['USER']
        form.select('#PASSWORD')[0]['value'] = self.common_data['PASSWORD']
        form.select('#target')[0]['value'] = res.json()['d']
        self.browser.session.headers.update(self.text_html)
        logged_in_page = self.browser.submit(
            form, '%s/ssologin/' % self.base_url)
        errors = logged_in_page.soup.select('#Error_Login .Error')
        if len(errors) == 0:
            self.logged_in = True
        else:
            raise PychexInvalidPasswordError(
                'The login information you entered does not match our '
                'records. Accounts will lock after 5 failed attempts to log '
                'on.')
        return self.logged_in

    def get_account_data(self):
        """ Get the Benefits OnLine app username via SOAP """

        if not self.logged_in:
            raise PychexUnauthenticatedError(
                'You must login before calling get_account_data')

        soap_content = open(os.path.join(
            os.path.dirname(__file__), 'templates',
            'GetUserApplicationAccountData.soap.xml')).read()
        data = soap_content.format(**self.common_data)
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
                self.app_username = account['{%s}ClientId' % service]
                return True
        raise PychexNoAppUsernameError(
            'Unable to retrieve Benefits OnLine app username')

    def get_account_summary(self):
        """ Get the 401k account summary """

        if not self.logged_in:
            raise PychexUnauthenticatedError(
                'You must login before calling get_account_summary')

        if not self.app_username:
            self.get_account_data()

        # Load the Benefits portal
        # SSOLogin
        res = self.browser.post(
            '%s/cgi-bin/contactus_es/ssologin_es' % self.benefits_url, data={
                'AppPass': self.common_data['PASSWORD'],
                'AppUsername': self.app_username
            })
        # Standard Login
        form = res.soup.select('form[name="PaychexStdLogin"]')[0]
        form['action'] = '%s/smlogin/login.fcc' % self.benefits_url
        self.browser.submit(form)

        # Load Retirement services app
        res = self.browser.get('%s/cgi-bin/401k/401kstart' % self.benefits_url)
        form = res.soup.select('form[name="PaychexSSNLogin"]')[0]
        form['action'] = '%s/401k_emp/do/LoginForm' % self.benefits_url
        self.browser.submit(form)

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
