"""
This file is for all tests related to the CLI client
"""

from httmock import urlmatch
from lettuce import step, world

from features.login.steps import mock_login_requests
from features.steps import mock_request
from mock import patch
from StringIO import StringIO

from pychex.cli import PychexCli


@urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
          path=r'.*?Butterfly.gif$')
def paychex_security_image_gif_mock(*args):
    """ Mock for the URL that retrieves the Paychex login security image """
    return open('./features/templates/Butterfly.gif').read()


@step(r'I run the authorize command$')
def authorize(step_arg):
    """ Test running the authorize method """
    with mock_login_requests():
        with patch('pychex.cli.PychexCli.get_input') as input_mock:
            with patch('getpass.getpass') as getpass_mock:
                with patch('PIL.Image.open'):
                    with patch.object(StringIO, '__init__') as stringio_mock:
                        with mock_request(paychex_security_image_gif_mock):
                            getpass_mock.return_value = world.password
                            input_mock.return_value = 'y'
                            stringio_mock.return_value = None
                            arguments = {
                                'authorize': True,
                                '--config': './pychex.cfg',
                                '<username>': world.username
                            }
                            pychex_cli = PychexCli(arguments)
                            input_mock.assert_called_once_with(
                                "Is this your security image (Y/n)? ")
                            gif_file = './features/templates/Butterfly.gif'
                            with open(gif_file) as gif:
                                img_dat = gif.read()
                            stringio_mock.assert_called_once_with(img_dat)
                            getpass_mock.assert_called_once_with(
                                "Password (input hidden): ")
                            assert pychex_cli.username == world.username


@step(r'the (.*) file should contain the encrypted credentials$')
def cfg_credentials(step_arg, config_file):
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
    assert pychex_cli.username == world.username
    assert pychex_cli.security_image_path == world.security_image_path
    assert pychex_cli.password == world.password
    # Check that the unencrypted values are not present
    with open(arguments['--config']) as cfg:
        cfg_txt = cfg.read()
    assert cfg_txt.find(world.username) == -1
    assert cfg_txt.find(world.security_image_path) == -1
    assert cfg_txt.find(world.password) == -1
