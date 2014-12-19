"""
This file is for tests related to Paychex object creation, and basic utilities
used by other modules
"""

import json

from behave import given, step
from nose.tools import assert_equals
from requests.adapters import HTTPAdapter
from requests.sessions import Session

from pychex import Paychex


@given('I create a Paychex object')
def create_paychex(context):
    """ Test creating a paychex object """
    context.paychex = Paychex(context.username)


@step('I create a Paychex object with username and security image')
def create_paychex_w_security(context):
    """ Test creating a paychex object with security_image_path """
    context.paychex = Paychex(context.username, context.security_image_path)


@step('I create a Paychex object with username and the wrong security image')
def create_paychex_w_wrong_security(context):
    """ Test creating a paychex object with the wrong security_image_path """
    context.paychex = Paychex(context.username, '/bad/image/path.gif')


@step('the Paychex object contains the needed urls')
def paychex_urls(context):
    """ Check that the Paychex object has the URLs it needs """
    assert context.paychex.start_url == 'https://www.mypaychex.com'
    base_url = 'https://landing.paychex.com'
    assert context.paychex.base_url == base_url
    assert context.paychex.login_url == '%s/ssologin/Login.aspx' % base_url
    assert context.paychex.benefits_url == 'https://benefits.paychex.com'


@step('the Paychex object contains content-type shortcuts')
def content_types(context):
    """ Check that the Paychex object has the content-types it needs """
    content_type = {'content-type': 'application/json; charset=utf-8'}
    assert context.paychex.app_json == content_type
    content_type['content-type'] = 'text/html; charset=utf-8'
    assert context.paychex.text_html == content_type


@step('the Paychex object contains a session')
def contains_session(context):
    """ Check that the Paychex object has a session """
    assert type(context.paychex.browser.session) == Session
    assert type(context.paychex.adapter) == HTTPAdapter
    assert context.paychex.adapter.max_retries.total == 3
    text_html = context.paychex.text_html['content-type']
    assert context.paychex.browser.session.headers['content-type'] == text_html


@step('the Paychex object contains initialized common_data')
def initialized_common_data(context):
    """ Check that the Paychex object has the expected common_data """
    assert_equals(context.paychex.common_data, {"USER": context.username})


@step('the Paychex object contains the correct security image path')
def initialized_security_image_path(context):
    """
    Check that the Paychex object contains the correct security image path
    """
    assert_equals(context.paychex.security_image_path,
                  context.security_image_path)


@step('the get_security_image method returns the full security image url')
def get_security_image(context):
    """
    Check that the get_security_image method returns the full security image
    url
    """
    sec_url = 'https://landing.paychex.com%s' % context.security_image_path
    assert context.paychex.get_security_image() == sec_url


@step('the Paychex object contains a {name} member variable set to {value}')
def paychex_variable(context, name, value):
    _paychex_variable(context, name, value)


@step('while mocking, the Paychex object contains a {name} member variable '
      'set to {value}')
def paychex_variable_while_mocking(context, name, value):
    _paychex_variable(context, name, value, mocking_only=True)


def _paychex_variable(context, name, value, mocking_only=False):
    """
    Check that a boolean, None, string, or dict variable matches what is
    given in the scenario
    """
    if mocking_only and not context.mock_requests:
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
    assert_equals(getattr(context.paychex, name), value)


@step('we have raised an exception:{exception_type}')
def raised_exception(context, exception_type):
    """ Check that the expected exception was raised in all cases """
    _raised_exception(context, exception_type)


@step('while mocking, we have raised an exception:{exception_type}')
def raised_exception_while_mocking(context, exception_type):
    """ Check that the expected exception was raised only if mocking """
    _raised_exception(context, exception_type, mocking_only=True)


def _raised_exception(context, exception_type, mocking_only=False):
    """ Check that the expected exception was raised """
    if mocking_only and not context.mock_requests:
        # Skip this test if we are not mocking requests
        return
    raised = False
    for exception in context.exceptions:
        if type(exception).__name__ == exception_type:
            raised = True
    assert raised, 'The expected exception was not raised'


@step('we have raised no exceptions')
def raised_no_exceptions(context):
    """ Check that no exceptions have been raised """
    assert len(context.exceptions) == 0
