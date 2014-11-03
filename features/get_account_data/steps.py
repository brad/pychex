"""
This file is for all tests related to the get_account_data method
"""

import sys

from httmock import urlmatch
from lettuce import step, world

from features.login.steps import mock_login_requests
from features.steps import mock_request
from pychex.exceptions import (
    PychexNoAppUsernameError,
    PychexUnauthenticatedError
)


@urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
                 path=r'(.*)?OneSourceService.asmx$')
def paychex_account_data_url_mock(*args):
    """
    Mock requests to the Paychex SOAP endpoint for retrieving account data
    """
    postfix = '' if world.has_bol else '_no_BOL'
    temp_dir = './features/templates/'
    filename = 'GetUserApplicationAccountDataResponse%s.soap.xml' % postfix
    return open('%s%s' % (temp_dir, filename)).read()


@step(r'I call the get_account_data method$')
def get_account_data(step_arg):
    """ Test calling get_account_data """
    _get_account_data()


@step(r'I call the get_account_data method with no BOL account$')
def get_account_data_no_bol(step_arg):
    """
    Test calling get_account_data on a user with no Benefits OnLine account
    """
    _get_account_data(has_bol=False)


def _get_account_data(has_bol=True):
    """
    Utility method to call get_account_data with or without a Benefits
    OnLine account
    """
    world.has_bol = has_bol
    with mock_login_requests():
        with mock_request(paychex_account_data_url_mock):
            try:
                assert world.paychex.get_account_data()
            except (PychexNoAppUsernameError, PychexUnauthenticatedError):
                world.exceptions.append(sys.exc_info()[1])


@step(r'the Paychex object contains an app_username member variable with '
      'the correct value')
def app_username_filled(step_arg):
    """ Check that the app_username variable has the info we expect """
    assert world.paychex.app_username is not None
    assert world.paychex.app_username == world.app_username
