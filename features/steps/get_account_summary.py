"""
This file is for all tests related to the get_account_summary method
"""

import json
import sys

from behave import step
from nose.tools import assert_equals

from pychex.exceptions import (
    PychexNoAppUsernameError,
    PychexUnauthenticatedError
)

from mocks import (
    ContextXmlMock,
    mock_benefits_requests,
    mock_login_requests,
    mock_request
)


@step('I call the get_account_summary method')
def get_account_summary(context):
    """ Test calling the get_account_summary """
    with mock_login_requests(context):
        mock_obj = ContextXmlMock(context)
        with mock_request(context, mock_obj.paychex_account_data):
            with mock_benefits_requests(context):
                try:
                    assert context.paychex.get_account_summary()
                except (PychexUnauthenticatedError, PychexNoAppUsernameError):
                    context.exceptions.append(sys.exc_info()[1])


@step('the Paychex object contains a balance_tab_info member variable '
      'with the following data')
def paychex_data(context):
    """ Check that the data in the scenario matches the data we extracted """
    if not context.mock_requests:
        # Skip this test since we are using real requests
        return
    data = {}
    for datum in context.table:
        data[datum['symbol']] = dict(datum.items())
        data[datum['symbol']]['fund'] = json.loads(datum['fund'])
    assert_equals(data, context.paychex.balance_tab_info)
