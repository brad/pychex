"""
This file is for all tests related to the CLI client
"""
from behave import step
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


@step('I run the authorize command')
def authorize(context):
    """ Test running the authorize method """
    with mock_login_requests(context):
        with patch('pychex.cli.PychexCli.get_input') as input_mock:
            with patch('getpass.getpass') as getpass_mock:
                with patch('PIL.Image.open') as image_open_mock:
                    with mock_request(context, FileMock().security_image_gif):
                        getpass_mock.return_value = context.password
                        input_mock.return_value = 'y'
                        arguments = {
                            'authorize': True,
                            '--config': './pychex-test.cfg',
                            '<username>': context.username
                        }
                        pychex_cli = PychexCli(arguments)
                        input_mock.assert_called_once_with(
                            "Is this your security image (Y/n)? ")
                        assert image_open_mock.call_count == 1
                        getpass_mock.assert_called_once_with(
                            "Password (input hidden): ")
                        assert pychex_cli.username == context.username


@step('the {config_file} file should contain the encrypted credentials')
def cfg_credentials(context, config_file):
    """ Check the credentials in the config file """
    arguments = {
        '--config': './%s' % config_file,
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
                    '--config': './pychex-test.cfg'
                }
                PychexCli(arguments)


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
