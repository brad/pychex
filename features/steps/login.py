"""
This file is for all tests related to the login method
"""
from __future__ import unicode_literals

import sys

from behave import step

from pychex.exceptions import (
    PychexSecurityImageMissingError,
    PychexInvalidPasswordError
)

from mocks import mock_login_requests


@step('I call the login method')
def login(context):
    """ Test calling the login method """
    _login(context, context.password)


@step('I call the login method with the wrong password')
def login_with_wrong_password(context):
    """ Test calling the login method with the wrong password """
    _login(context, 'BAD_PASSWORD')


def _login(context, password):
    """ Call the login method with the provided password """
    with mock_login_requests(context):
        try:
            assert context.paychex.login(password)
        except (PychexInvalidPasswordError, PychexSecurityImageMissingError):
            context.exceptions.append(sys.exc_info()[1])
