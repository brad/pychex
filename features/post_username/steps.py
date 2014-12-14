"""
This file is for testing all features related to the post_username method
"""

import json
import sys

from httmock import urlmatch
from lettuce import step, world

from features.steps import mock_request
from features.session.steps import paychex_start_url_mock
from pychex.exceptions import (
    PychexSecurityImageMismatchError,
    PychexSecurityImageMissingError
)


@urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
          path=r'.*?GetSecurityImage$')
def paychex_security_image_url_mock(*args):
    """ Mock for the URL that retrieves the Paychex login security image """
    return json.dumps({'d': world.security_image_path})


@step(r'I call the post_username method')
def post_username(step_arg):
    """ Test calling the post_username method """
    with mock_request(paychex_start_url_mock):
        with mock_request(paychex_security_image_url_mock):
            try:
                world.paychex.post_username()
            except PychexSecurityImageMismatchError:
                world.exceptions.append(sys.exc_info()[1])


@step(r'I call the get_security_image method')
def get_security_image_missing(step_arg):
    """ Test calling the get_security_image method """
    try:
        world.paychex.get_security_image()
    except PychexSecurityImageMissingError:
        world.exceptions.append(sys.exc_info()[1])
