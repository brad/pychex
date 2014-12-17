"""
This file is for all tests related to the get_account_data method
"""

import sys

from behave import step

from pychex.exceptions import (
    PychexNoAppUsernameError,
    PychexUnauthenticatedError
)

from mocks import ContextXmlMock, mock_login_requests, mock_request


@step('I call the get_account_data method')
def get_account_data(context):
    """ Test calling get_account_data """
    _get_account_data(context)


@step('I call the get_account_data method with no BOL account')
def get_account_data_no_bol(context):
    """
    Test calling get_account_data on a user with no Benefits OnLine account
    """
    _get_account_data(context, has_bol=False)


def _get_account_data(context, has_bol=True):
    """
    Utility method to call get_account_data with or without a Benefits
    OnLine account
    """
    context.has_bol = has_bol
    with mock_login_requests(context):
        with mock_request(context,
                          ContextXmlMock(context).paychex_account_data):
            try:
                assert context.paychex.get_account_data()
            except (PychexNoAppUsernameError, PychexUnauthenticatedError):
                context.exceptions.append(sys.exc_info()[1])


@step('the Paychex object contains an app_username member variable with '
      'the correct value')
def app_username_filled(context):
    """ Check that the app_username variable has the info we expect """
    assert context.paychex.app_username is not None
    assert context.paychex.app_username == context.app_username
