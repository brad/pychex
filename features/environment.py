"""
Place globals in this file. We will attempt to import from a local environment
file called environment_NOCOMMIT.py which is ignored by git. Any environment
overrides belong in this file. It is your responsibility to protect any
sensitive data stored in that file and DO NOT commit it to git. To run the
tests with real HTTP requsests on your own Paychex account, create a
environment_NOCOMMIT.py file with contents similar to the following:

# Local terrain overrides
MOCK_REQUESTS = False
if not MOCK_REQUESTS:
    USERNAME = 'YOUR_USERNAME'
    SECURITY_IMAGE_PATH = '/ssologin/Media/Images/Security/YOUR_IMAGE.gif'
    PASSWORD = 'YOUR_PASSWORD'
    APP_USERNAME = 'YOUR_APP_USERNAME'   # Obtained by get_account_data
"""

MOCK_REQUESTS = True
USERNAME = 'FAKE_USERNAME'
SECURITY_IMAGE_PATH = '/ssologin/Media/Images/Security/Butterfly.gif'
PASSWORD = 'FAKE_PASSWORD'
APP_USERNAME = 'FAKE_USERNAME_BOL'

try:
    from features.environment_NOCOMMIT import *
except ImportError:
    pass


def before_all(context):
    context.mock_requests = MOCK_REQUESTS
    context.username = USERNAME
    context.security_image_path = SECURITY_IMAGE_PATH
    context.password = PASSWORD
    context.app_username = APP_USERNAME
    context.config_file = './pychex-test.cfg'

    context.exceptions = []
    context.has_bol = True
    context.do_coverage = True


def before_scenario(context, scenario):
    """ Reset some global variables to default """
    context.exceptions = []
    context.has_bol = True
    return context
