"""
This file is for all tests related to the get_bol_username method
"""

import sys

from behave import step

from pychex.exceptions import (
    PychexNoBolUsernameError,
    PychexUnauthenticatedError
)

from mocks import ContextXmlMock, mock_login_requests, mock_request


@step('I call the get_bol_username method')
def get_bol_username(context):
    """ Test calling get_bol_username """
    _get_bol_username(context)


@step('I call the get_bol_username method with no BOL account')
def get_bol_username_no_bol(context):
    """
    Test calling get_bol_username on a user with no Benefits OnLine account
    """
    _get_bol_username(context, has_bol=False)


def _get_bol_username(context, has_bol=True):
    """
    Utility method to call get_bol_username with or without a Benefits
    OnLine account
    """
    context.has_bol = has_bol
    with mock_login_requests(context):
        with mock_request(context,
                          ContextXmlMock(context).paychex_account_data):
            try:
                return context.paychex.get_bol_username()
            except (PychexNoBolUsernameError, PychexUnauthenticatedError):
                context.exceptions.append(sys.exc_info()[1])


@step('the get_bol_username method returns the correct bol_username')
def bol_username_returned(context):
    """ Check that the get_bol_username method returns the correct thing """
    bol_username = _get_bol_username(context)
    assert bol_username is not None
    assert bol_username == context.bol_username
