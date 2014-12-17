"""
This file is for testing all features related to the post_username method
"""

import sys

from behave import step

from pychex.exceptions import (
    PychexSecurityImageMismatchError,
    PychexSecurityImageMissingError
)

from mocks import ContextJsonMock, HtmlMock, mock_request


@step('I call the post_username method')
def post_username(context):
    """ Test calling the post_username method """
    with mock_request(context, HtmlMock().paychex_start):
        mock_obj = ContextJsonMock(context)
        with mock_request(context, mock_obj.paychex_security_image):
            try:
                context.paychex.post_username()
            except PychexSecurityImageMismatchError:
                context.exceptions.append(sys.exc_info()[1])


@step('I call the get_security_image method')
def get_security_image_missing(context):
    """ Test calling the get_security_image method """
    try:
        context.paychex.get_security_image()
    except PychexSecurityImageMissingError:
        context.exceptions.append(sys.exc_info()[1])
