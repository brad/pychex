"""
This file is for all tests related to the login method
"""

import json
import sys

from httmock import urlmatch
from lettuce import step, world

from contextlib import contextmanager
from features.post_username.steps import paychex_security_image_url_mock
from features.session.steps import paychex_start_url_mock
from features.steps import mock_request
from pychex.exceptions import (
    PychexSecurityImageMissingError,
    PychexInvalidPasswordError
)


@urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
          path=r'(.*)?ProcessLogin$')
def paychex_process_login_url_mock(*args):
    """ Mock requests to the Paychex ProcessLogin URL """
    return json.dumps({'d': '/LandingRedirect.aspx'})


@urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
          path=r'(.*)?login\.fcc$')
def paychex_login_url_mock(*args):
    """ Mock requests to the Paychex login.fcc URL """
    if world.paychex.common_data['PASSWORD'] == world.password:
        return '<html></html>'
    else:
        return open('./features/templates/paychex_login_invalid.fcc').read()


@step(r'I call the login method$')
def login(step_arg):
    """ Test calling the login method """
    _login(world.password)


@step(r'I call the login method with the wrong password')
def login_with_wrong_password(step_arg):
    """ Test calling the login method with the wrong password """
    _login('BAD_PASSWORD')


def _login(password):
    """ Call the login method with the provided password """
    with mock_login_requests():
        try:
            assert world.paychex.login(password)
        except (PychexInvalidPasswordError, PychexSecurityImageMissingError):
            world.exceptions.append(sys.exc_info()[1])


@contextmanager
def mock_login_requests():
    """ Helper method to mock all requests needed for logging in """
    with mock_request(paychex_start_url_mock):
        with mock_request(paychex_security_image_url_mock):
            with mock_request(paychex_process_login_url_mock):
                with mock_request(paychex_login_url_mock):
                    yield
