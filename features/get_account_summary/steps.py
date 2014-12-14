"""
This file is for all tests related to the get_account_summary method
"""

import json
import sys

from contextlib import contextmanager
from httmock import urlmatch
from lettuce import step, world
from nose.tools import assert_equals

from features.get_account_data.steps import paychex_account_data_url_mock
from features.login.steps import mock_login_requests
from features.steps import mock_request
from pychex.exceptions import (
    PychexNoAppUsernameError,
    PychexUnauthenticatedError
)


@urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
          path=r'.*?ssologin_es$')
def paychex_benefits_sso_url_mock(*args):
    """ Mock requests to the benefits ssologin_es URL """
    return open('./features/templates/benefits_ssologin_es.html').read()


@urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
          path=r'.*?login\.fcc$')
def paychex_benefits_login_url_mock(*args):
    """ Mock requests to the benefits login.fcc URL """
    return ''


@urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
          path=r'.*?401kstart$')
def paychex_401k_start_url_mock(*args):
    """ Mock requests to the retirement app 401kstart URL """
    return open('./features/templates/401kstart.html').read()


@urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
          path=r'.*?LoginForm$')
def paychex_401k_login_url_mock(*args):
    """ Mock requests to the retirement app LoginForm URL """
    return ''


@urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
          path=r'.*?accountSummary$')
def paychex_401k_summary_url_mock(*args):
    """ Mock requests to the retirement app accountSummary URL """
    return open('./features/templates/accountSummary.html').read()


@urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
          path=r'.*?getBalanceTab$')
def paychex_401k_balance_url_mock(*args):
    """ Mock requests to the retirement app getBalanceTab URL """
    return open('./features/templates/getBalanceTab.html').read()


@step(r'I call the get_account_summary method$')
def get_account_summary(step_arg):
    """ Test calling the get_account_summary """
    with mock_login_requests():
        with mock_request(paychex_account_data_url_mock):
            with mock_benefits_requests():
                try:
                    assert world.paychex.get_account_summary()
                except (PychexUnauthenticatedError, PychexNoAppUsernameError):
                    world.exceptions.append(sys.exc_info()[1])


@step(r'the Paychex object contains a balance_tab_info member variable '
      'with the following data')
def paychex_data(step_arg):
    """ Check that the data in the scenario matches the data we extracted """
    if not world.mock_requests:
        # Skip this test since we are using real requests
        return
    data = {}
    for datum in step_arg.hashes:
        data[datum['symbol']] = datum
        data[datum['symbol']]['fund'] = json.loads(datum['fund'])
    assert_equals(data, world.paychex.balance_tab_info)


@contextmanager
def mock_benefits_requests():
    """ Helper to mock all requests made in the get_account_summary method """
    with mock_request(paychex_benefits_sso_url_mock):
        with mock_request(paychex_benefits_login_url_mock):
            with mock_request(paychex_401k_start_url_mock):
                with mock_request(paychex_401k_login_url_mock):
                    with mock_request(paychex_401k_summary_url_mock):
                        with mock_request(paychex_401k_balance_url_mock):
                            yield
