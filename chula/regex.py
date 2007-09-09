"""
Common regular expressions
"""

import re

def match(regex, test):
    if re.search(regex, test) is None:
        return False
    else:
        return True

IPV4 = (r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)'
        r'{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')

PASSWD = r'^[-a-zA-Z0-9!@#$%^&?.*]{6,}$'

EMAIL = (r'^[a-z0-9_\-]+(\.[_a-z0-9\-]+)*'
         r'@([_a-z0-9\-]+\.)+([a-z]{2}'
         r'|aero|arpa|biz|com|coop|edu|gov|info|int|jobs|mil'
         r'|museum|name|nato|net|org|pro|travel)$')

SCRIPTS_STAMP = (r'^(19|20|21|22)\d\d(0[1-9]|1[012])'
                 r'(0[1-9]|[12][0-9]|3[01])-([01][1-9]|[01][0-9]|2[0-3])\.'
                 r'([0-5][0-9]|60)\.([0-5][0-9]|60)')

SCRIPTS_BACKUP = SCRIPTS_STAMP + r'.*\.tar\.gz'
SCRIPTS_LOG = SCRIPTS_STAMP + r'.*\.log'

_TAG = 'a-zA-Z0-9-_'
TAG  = r'^([%s])+$' % _TAG
TAGS = r'^([%s]\s{0,1})+$' % _TAG

