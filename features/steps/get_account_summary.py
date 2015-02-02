"""
This file is for all tests related to the get_account_summary method
"""

import json
import sys

from behave import step
from nose.tools import assert_equals

from pychex.exceptions import (
    PychexNoBolUsernameError,
    PychexUnauthenticatedError
)

from mocks import (
    ContextXmlMock,
    mock_benefits_requests,
    mock_login_requests,
    mock_request
)


@step('I call the RetirementServices.get_account_summary method')
def get_account_summary(context):
    """ Test calling the RetirementServices.get_account_summary method """
    with mock_benefits_requests(context):
        try:
            retirement = context.benefits_online.retirement_services
            assert retirement.get_account_summary()
        except PychexUnauthenticatedError:
            context.exceptions.append(sys.exc_info()[1])


@step('the RetirementServices object contains a balance_tab_info member '
      'variable with the following data')
def rs_data(context):
    """ Check that the data in the scenario matches the data we extracted """
    if not context.mock_requests:
        # Skip this test since we are using real requests
        return
    data = {}
    for datum in context.table:
        data[datum['symbol']] = dict(datum.items())
        data[datum['symbol']]['fund'] = json.loads(datum['fund'])
    retirement = context.benefits_online.retirement_services
    assert_equals(data, retirement.balance_tab_info)
