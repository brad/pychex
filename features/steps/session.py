"""
This file is for all tests related to setting up a Paychex session
"""

from behave import step

from mocks import HtmlMock, mock_request


@step('I call the initialize_session method')
def initialize_session(context):
    """ Test calling the initialize_session method """
    with mock_request(context, HtmlMock().paychex_start_url):
        context.paychex.initialize_session()


@step('the Paychex object contains the necessary session state')
def session_state(context):
    """ Test that the paychex object contains the expected session data """
    assert hasattr(context.paychex, 'login_page')


@step('the Paychex object does not contain the necessary session state')
def no_session_state(context):
    """ Test that the paychex object does not contain any session data """
    assert hasattr(context.paychex, 'login_page') is False
