"""
This file is for tests related to Paychex object creation, and basic utilities
used by other modules
"""

import json

from behave import given, step
from nose.tools import assert_equals
from requests.adapters import HTTPAdapter
from requests.sessions import Session

from pychex import Paychex, BenefitsOnline


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


@given('I create a BenefitsOnline object')
def create_benefits_online(context):
    """ Test creating a BenifitsOnline object """
    context.benefits_online = BenefitsOnline(context.bol_username,
                                             context.password)


@step('the BenefitsOnline object contains the needed urls')
def benefits_online_urls(context):
    """ Check that the RetirementServices object has the URLs it needs """
    assert context.benefits_online.benefits_url == \
        'https://benefits.paychex.com'


@step('the RetirementServices object contains the needed urls')
def retirement_services_urls(context):
    """ Check that the RetirementServices object has the URLs it needs """
    assert context.benefits_online.retirement_services.benefits_url == \
        'https://benefits.paychex.com'


@step('the Paychex object contains content-type shortcuts')
def content_types(context):
    """ Check that the Paychex object has the content-types it needs """
    content_type = {'content-type': 'text/html; charset=utf-8'}
    assert context.paychex.text_html == content_type


@step('the Paychex object contains a session')
def paychex_contains_sessions(context):
    """ Check that the Paychex object has a session """
    _contains_session(context.paychex)


@step('the BenefitsOnline object contains a session')
def bol_contains_sessions(context):
    """ Check that the BenifitsOnline object has a session """
    _contains_session(context.benefits_online)


@step('the RetirementServices object contains a session')
def rs_contains_sessions(context):
    """ Check that the RetirementServices object has a session """
    _contains_session(context.benefits_online.retirement_services)


def _contains_session(obj):
    """ Check that the specified object has a session """
    assert type(obj.browser.session) == Session
    assert type(obj.adapter) == HTTPAdapter
    assert obj.adapter.max_retries.total == 3
    text_html = obj.text_html['content-type']
    assert obj.browser.session.headers['content-type'] == text_html


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
    _obj_variable(context, context.paychex,  name, value)


@step('while mocking, the Paychex object contains a {name} member variable '
      'set to {value}')
def paychex_variable_while_mocking(context, name, value):
    _obj_variable(context, context.paychex, name, value, mocking_only=True)


@step('the BenefitsOnline object contains a {name} member variable set to '
      '{value}')
def benefits_online_variable(context, name, value):
    _obj_variable(context, context.benefits_online,  name, value)


@step('the BenefitsOnline object contains a {name} member variable of '
      'type:{var_type}')
def benefits_online_variable_type(context, name, var_type):
    assert_equals(getattr(context.benefits_online, name).__class__.__name__,
                  var_type)


@step('the RetirementServices object contains a {name} member variable set to '
      '{value}')
def retirement_services_variable(context, name, value):
    _obj_variable(context, context.benefits_online.retirement_services, name,
                  value)


@step('while mocking, the RetirementServices object contains a {name} member '
      'variable set to {value}')
def rs_variable_while_mocking(context, name, value):
    _obj_variable(context, context.benefits_online.retirement_services, name,
                  value, mocking_only=True)


def _obj_variable(context, obj, name, value, mocking_only=False):
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
    assert_equals(getattr(obj, name), value)


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
