"""
Place globals in this file. We will attempt to import from a local terrain
file called terrain_NOCOMMIT.py which is ignored by git. Any terrain
overrides belong in this file. It is your responsibility to protect any
sensitive data stored in that file and DO NOT commit it to git. To run the
tests with real HTTP requsests on your own Paychex account, create a
terrain_NOCOMMIT.py file with contents similar to the following:

# Local terrain overrides
MOCK_REQUESTS = False
if not MOCK_REQUESTS:
    USERNAME = 'YOUR_USERNAME'
    SECURITY_IMAGE_PATH = '/ssologin/Media/Images/Security/YOUR_IMAGE.gif'
    PASSWORD = 'YOUR_PASSWORD'
    APP_USERNAME = 'YOUR_APP_USERNAME'   # Obtained by get_account_data
"""

from lettuce import world

MOCK_REQUESTS = True
USERNAME = 'FAKE_USERNAME'
SECURITY_IMAGE_PATH = '/ssologin/Media/Images/Security/Butterfly.gif'
PASSWORD = 'FAKE_PASSWORD'
APP_USERNAME = 'FAKE_USERNAME_BOL'

try:
    from features.terrain_NOCOMMIT import *
except ImportError:
    pass

world.mock_requests = MOCK_REQUESTS
world.username = USERNAME
world.security_image_path = SECURITY_IMAGE_PATH
world.password = PASSWORD
world.app_username = APP_USERNAME

world.exceptions = []
world.has_bol = True
world.do_coverage = True
