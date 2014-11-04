"""
This file is for tests related to Paychex object creation, and basic utilities
used by other modules
"""

import coverage
import json
import os

from contextlib import contextmanager
from httmock import HTTMock
from lettuce import after, before, step, world
from nose.tools import assert_equals
from requests.adapters import HTTPAdapter
from requests.sessions import Session

from pychex import Paychex


@after.each_scenario
def after_each_scenario(scenario):
    """ Reset some global variables to default """
    world.exceptions = []
    world.has_bol = True


@step(r'I create a Paychex object$')
def create_paychex(step_arg):
    """ Test creating a paychex object """
    world.paychex = Paychex(world.username)


@step(r'I create a Paychex object with username and security image')
def create_paychex_w_security(step_arg):
    """ Test creating a paychex object with security_image_path """
    world.paychex = Paychex(world.username, world.security_image_path)


@step(r'I create a Paychex object with username and the wrong security image')
def create_paychex_w_wrong_security(step_arg):
    """ Test creating a paychex object with the wrong security_image_path """
    world.paychex = Paychex(world.username, '/bad/image/path.gif')


@step(r'the Paychex object contains the needed urls')
def paychex_urls(step_arg):
    """ Check that the Paychex object has the URLs it needs """
    assert world.paychex.start_url == 'https://www.mypaychex.com'
    base_url = 'https://landing.paychex.com'
    assert world.paychex.base_url == base_url
    assert world.paychex.login_url == '%s/ssologin/Login.aspx' % base_url
    assert world.paychex.benefits_url == 'https://benefits.paychex.com'


@step(r'the Paychex object contains content-type shortcuts')
def content_types(step_arg):
    """ Check that the Paychex object has the content-types it needs """
    content_type = {'content-type': 'application/json; charset=utf-8'}
    assert world.paychex.app_json == content_type
    content_type['content-type'] = 'text/html; charset=utf-8'
    assert world.paychex.text_html == content_type


@step(r'the Paychex object contains a session')
def contains_session(step_arg):
    """ Check that the Paychex object has a session """
    assert type(world.paychex.session) == Session
    assert type(world.paychex.adapter) == HTTPAdapter
    assert world.paychex.adapter.max_retries == 3
    text_html = world.paychex.text_html['content-type']
    assert world.paychex.session.headers['content-type'] == text_html


@step(r'the Paychex object contains initialized common_data')
def initialized_common_data(step_arg):
    """ Check that the Paychex object has the expected common_data """
    assert_equals(world.paychex.common_data, {"USER": world.username})


@step(r'the Paychex object contains the correct security image path')
def initialized_security_image_path(step_arg):
    """
    Check that the Paychex object contains the correct security image path
    """
    assert_equals(world.paychex.security_image_path, world.security_image_path)


@step(r'the get_security_image method returns the full security image url')
def get_security_image(step_arg):
    """
    Check that the get_security_image method returns the full security image url
    """
    sec_url = 'https://landing.paychex.com%s' % world.security_image_path
    assert world.paychex.get_security_image() == sec_url


@step(r'the Paychex object contains a (.*) member variable set to (\S+)$')
def paychex_variable(step_arg, name, value):
    _paychex_variable(name, value)


@step(r'the Paychex object contains a (.*) member variable set to (\S+) while mocking')
def paychex_variable_while_mocking(step_arg, name, value):
    _paychex_variable(name, value, mocking_only=True)


def _paychex_variable(name, value, mocking_only=False):
    """
    Check that a boolean, None, string, or dict variable matches what is
    given in the scenario
    """
    if mocking_only and not world.mock_requests:
        # Skip this test if we are not mocking requests
        return
    if not value.startswith('"'):
        if value == 'None':
            value = None
        elif value == 'True' or value == 'False':
            value = value == 'True'
        else:
            value = json.loads(value)
    else:
        value = value.replace('"', '')
    assert_equals(getattr(world.paychex, name), value)


@step(r'we have raised an exception:([a-zA-Z]+)$')
def raised_exception(step_arg, exception_type):
    """ Check that the expected exception was raised in all cases """
    _raised_exception(exception_type)


@step(r'we have raised an exception:([a-zA-Z]+) while mocking$')
def raised_exception_while_mocking(step_arg, exception_type):
    """ Check that the expected exception was raised only if mocking """
    _raised_exception(exception_type, mocking_only=True)


def _raised_exception(exception_type, mocking_only=False):
    """ Check that the expected exception was raised, only if mocking  """
    if mocking_only and not world.mock_requests:
        # Skip this test if we are not mocking requests
        return
    raised = False
    for exception in world.exceptions:
        if type(exception).__name__ == exception_type:
            raised = True
    assert raised, 'The expected exception was not raised'


@step(r'we have raised no exceptions')
def raised_no_exceptions(step_arg):
    """ Check that no exceptions have been raised """
    assert len(world.exceptions) == 0


@contextmanager
def mock_request(mock_func):
    """
    Helper method to mock the HTTP request when world.mock_requests is True,
    or otherwise do a real request.
    """

    if world.mock_requests:
        with HTTMock(mock_func):
            yield
    else:
        yield
