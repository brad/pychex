"""
This file is for all tests related to setting up a Paychex session
"""

from httmock import urlmatch
from lettuce import step, world

from features.steps import mock_request


@urlmatch(scheme='https', netloc=r'www\.mypaychex\.com$')
def paychex_start_url_mock(*args):
    """ Mock requests to the Paychex login page URL """
    return open('./features/templates/paychex_login.aspx').read()


@step(r'I call the initialize_session method')
def initialize_session(step_arg):
    """ Test calling the initialize_session method """
    with mock_request(paychex_start_url_mock):
        world.paychex.initialize_session()


@step(r'the Paychex object contains the necessary session state')
def session_state(step_arg):
    """ Test that the paychex object contains the expected session data """
    for key in ['SMENC', 'SMLOCALE', '__VIEWSTATE', '__EVENTVALIDATION']:
        assert key in world.paychex.common_data
        if world.mock_requests:
            assert world.paychex.common_data[key] == 'FAKE_%s' % key


@step(r'the Paychex object does not contain the necessary session state')
def no_session_state(step_arg):
    """ Test that the paychex object does not contain any session data """
    for key in ['SMENC', 'SMLOCALE', '__VIEWSTATE', '__EVENTVALIDATION']:
        assert key not in world.paychex.common_data
