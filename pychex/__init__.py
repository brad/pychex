"""
Pychex is a library which provides read-only programmatic and CLI access to
account information for Paychex Benefits OnLine accounts. The command-line
client serves as an example for anyone who wishes to build their own client
(hint: Mint). To get started using the client, see :ref:`CLI-usage`.
"""

from pychex.paychex import *

__all__ = ['Paychex', 'BenefitsOnline']
__title__ = 'pychex'
__author__ = 'Brad Pitcher'
__author_email__ = 'bradpitcher@gmail.com'
__copyright__ = '2014-2015, Brad Pitcher'
__license__ = 'Apache 2.0'
__version__ = '0.4.0dev'
__release__ = __version__
