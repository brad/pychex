"""
This file is for all tests related to setting up a Paychex session
"""

from httmock import response, urlmatch
from lettuce import step, world

from features.steps import HtmlMock, mock_request


@urlmatch(scheme='https', netloc=r'www\.mypaychex\.com$')
def paychex_start_url_mock(url, request):
    """ Mock requests to the Paychex login page URL """
    # Change the URL since this results in a redirect
    request.url = 'https://landing.paychex.com/ssologin/login.aspx?params'
    res = HtmlMock().build_response('paychex_login.aspx')
    return response(200, res['content'], res['headers'], None, 5, request)


@step(r'I call the initialize_session method')
def initialize_session(step_arg):
    """ Test calling the initialize_session method """
    with mock_request(paychex_start_url_mock):
        world.paychex.initialize_session()


@step(r'the Paychex object contains the necessary session state')
def session_state(step_arg):
    """ Test that the paychex object contains a login_page """
    assert hasattr(world.paychex, 'login_page')


@step(r'the Paychex object does not contain the necessary session state')
def no_session_state(step_arg):
    """ Test that the paychex object does not have a login_page """
    assert hasattr(world.paychex, 'login_page') is False
