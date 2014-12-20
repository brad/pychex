"""
This file is for all tests related to the CLI client
"""
from __future__ import unicode_literals

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


@step('I run the account_summary command')
def run_account_summary(context):
    # Make sure the password check passes in the paychex_login mock
    context.paychex = MagicMock()
    context.paychex.common_data = {'PASSWORD': context.password}
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
                    '--config': context.config_file
                }
                try:
                    PychexCli(arguments)
                except:
                    pass


@step('I should see my account summary')
def print_account_summary(context):
    assert context.stdout_capture.getvalue() == \
"""Current balance: $XX,XXX.XX
Vested balance: $XX,XXX.XX
Personal RoR: X.X%

  percent  symbol    fund               shares  balance     prospectus
---------  --------  ---------------  --------  ----------  ------------
     9.79  FNAMW     FAKE NAME W [1]   103.572  $6,644.72   [2]
    10.21  FNAMX     FAKE NAME X [3]   214.321  $6,929.78   [4]
    31.58  FNAMY     FAKE NAME Y [5]    13.179  $21,434.13  [6]
    48.42  FNAMZ     FAKE NAME Z [7]    26.624  $32,863.86  [8]

[1] http://www.example.com/?product=FUNDS&custno=1&FUNDID=1
[2] http://www.example.com/?product=PROSP&custno=1&FUNDID=1
[3] http://www.example.com/?product=FUNDS&custno=1&FUNDID=2
[4] http://www.example.com/?product=PROSP&custno=1&FUNDID=2
[5] http://www.example.com/?product=FUNDS&custno=1&FUNDID=3
[6] http://www.example.com/?product=PROSP&custno=1&FUNDID=3
[7] http://www.example.com/?product=FUNDS&custno=1&FUNDID=4
[8] http://www.example.com/?product=PROSP&custno=1&FUNDID=4
"""


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
