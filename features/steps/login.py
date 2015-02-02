"""
This file is for all tests related to the login method
"""
from __future__ import unicode_literals

import sys

from behave import step

from pychex.exceptions import (
    PychexSecurityImageMissingError,
    PychexUnknownError,
    PychexInvalidPasswordError
)

from mocks import mock_benefits_requests, mock_login_requests


@step('I call the Paychex.login method')
def paychex_login(context):
    """ Test calling the Paychex.login method """
    _login(context, 'paychex', context.password)


@step('I call the Paychex.login method with the wrong password')
def paychex_login_with_wrong_password(context):
    """ Test calling the Paychex.login method with the wrong password """
    _login(context, 'paychex', 'BAD_PASSWORD')


@step('I call the BenefitsOnline.login method')
def bol_login(context):
    """ Test calling the BenefitsOnline.login method """
    _login(context, 'benefits_online', context.password)


@step('I call the BenefitsOnline.login method with the wrong password')
def bol_login_with_wrong_password(context):
    """ Test calling the BenefitsOnline.login method with the wrong pw """
    _login(context, 'benefits_online', 'BAD_PASSWORD')


@step('I call the RetirementServices.login method')
def rs_login(context):
    """ Test calling the RetirementServices.login method """
    _login(context, 'retirement_services')


@step('I get an error logging in to Retirement Services')
def rs_login_error(context):
    """ Test calling the RetirementServices.login method, with error """
    _login(context, 'retirement_services', http_status=500)


def _login(context, logging_into, password=None, http_status=200):
    """ Call the login method of the specified type of object """
    with mock_login_requests(context):
        with mock_benefits_requests(context, http_status):
            try:
                if logging_into == 'paychex':
                    assert context.paychex.login(password)
                elif logging_into == 'benefits_online':
                    context.benefits_online.password = password
                    assert context.benefits_online.login()
                else:
                    assert context.benefits_online.retirement_services.login()
            except (PychexInvalidPasswordError, PychexUnknownError,
                    PychexSecurityImageMissingError):
                context.exceptions.append(sys.exc_info()[1])
