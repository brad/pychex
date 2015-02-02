"""
This file is for all tests related to the CLI client
"""
from __future__ import unicode_literals

import sys

from behave import given, then, step
from mock import MagicMock

from pychex.cli import PychexCli

from mocks import (
    ContextXmlMock,
    FileMock,
    mock_benefits_requests,
    mock_login_requests,
    mock_request
)

try:
    from unittest.mock import patch
except ImportError:  # Python 2.x fallback
    from mock import patch


@given('I have not authorized the CLI')
def not_authorized(context):
    """
    Make sure the user isn't authorized by pointing to a non-existing config
    file
    """
    context.config_file = 'NON_EXISTENT_FILE.cfg'


@given('my config is missing the pychex section')
def missing_section(context):
    """ See what happens when the pychex section is missing from the config """
    context.config_file = './features/files/missing-section.cfg'


@given('my config is missing an option')
def missing_option(context):
    """ See what happens when an option is missing from the config """
    context.config_file = './features/files/missing-option.cfg'


@given('I answer "{answer}" to the security question during authorization')
def authorize_answer(context, answer):
    """ Test running the authorize method with a specific answer """
    context.security_answer = answer
    context.execute_steps('Given I run the authorize command')


@given('I answer "" to the security question during authorization')
def authorize_blank_answer(context):
    """ Test running the authorize method with a blank answer """
    context.security_answer = ''
    context.execute_steps('Given I run the authorize command')


@given('I run the authorize command')
@patch('PIL.Image.open')
@patch('getpass.getpass')
@patch('pychex.cli.PychexCli.get_input')
def authorize(context, input_mock, getpass_mock, image_open_mock):
    """ Test running the authorize method """
    with mock_login_requests(context):
        with mock_request(context, FileMock().security_image_gif):
            mock_func = ContextXmlMock(context).paychex_account_data
            with mock_request(context, mock_func):
                getpass_mock.return_value = context.password
                input_mock.return_value = context.security_answer
                arguments = {
                    'authorize': True,
                    '--config': context.config_file,
                    '<username>': context.username
                }
                pychex_cli = PychexCli(arguments)
                input_mock.assert_called_once_with(
                    'Is this your security image (Y/n)? ')
                assert image_open_mock.call_count == 1
                if context.security_answer in ['yes', 'y', 'ye', '']:
                    getpass_mock.assert_called_once_with(
                        'Password (input hidden): ')
                    assert pychex_cli.username == context.username


@step('the config file should contain the encrypted credentials')
def cfg_credentials(context):
    """ Check the credentials in the config file """
    arguments = {
        '--config': context.config_file,
        'authorize': False,
        'account_summary': False
    }
    pychex_cli = PychexCli(arguments)
    pychex_cli.read_config()
    # Check that the values pulled from the read_config method match what we
    # know
    print(pychex_cli.username)
    assert pychex_cli.username == context.username
    assert pychex_cli.security_image_path == context.security_image_path
    assert pychex_cli.password == context.password
    # Check that the unencrypted values are not present
    with open(arguments['--config']) as cfg:
        cfg_txt = cfg.read()
    assert cfg_txt.find(context.username) == -1
    assert cfg_txt.find(context.security_image_path) == -1
    assert cfg_txt.find(context.password) == -1


@step('I run the account_summary command with json output')
def run_account_summary_json(context):
    run_account_summary(context, json=True)


@step('I run the account_summary command')
def run_account_summary(context, json=False):
    # Make sure the password check passes in the paychex_login mock
    context.paychex = MagicMock()
    context.paychex.password = context.password
    # Reset the stdout capture
    context.stdout_capture.truncate(0)
    context.stdout_capture.seek(0)

    with mock_login_requests(context):
        mock_obj = ContextXmlMock(context)
        with mock_request(context, mock_obj.paychex_account_data):
            with mock_benefits_requests(context):
                arguments = {
                    'authorize': False,
                    'account_summary': True,
                    '--config': context.config_file,
                    '--json': json
                }
                try:
                    PychexCli(arguments)
                except Exception:
                    assert False, 'Exception: %s' % sys.exc_info()[1]


@step('I should see my account summary as json')
def print_account_summary_json(context):
    import json
    with open('./features/files/cli_fake_summary.json') as fake_summary_json:
        fake_summary_dict = json.loads(fake_summary_json.read())
    capture_value_dict = json.loads(context.stdout_capture.getvalue())
    assert capture_value_dict == fake_summary_dict, capture_value_dict


@step('I should see my account summary')
def print_account_summary(context, json=False):
    with open('./features/files/cli_fake_summary.txt') as fake_summary:
        fake_summary_str = fake_summary.read()
    capture_value = context.stdout_capture.getvalue()
    assert capture_value == fake_summary_str, capture_value


@then('we remind the user to authorize')
def authorize_reminder(context):
    assert context.stdout_capture.getvalue() == (
        'Error reading credentials, please run: pychex authenticate '
        '<username>\n')


@then('I should see a reminder to answer "yes" or "no"')
def answer_reminder(context):
    assert context.stdout_capture.getvalue() == (
        'Please respond with "yes" or "no".\n')


@then("I should see a notice that the security image didn't match")
def answer_reminder(context):
    assert context.stdout_capture.getvalue() == 'Security image mismatch.\n'
