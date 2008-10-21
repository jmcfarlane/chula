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

TAG_CHARS = r'a-zA-Z0-9-_'
TAG_MATCH = r'[%s]+' % TAG_CHARS
TAG  = r'^%s$' % TAG_MATCH
TAGS = r'^%s((, ?| )+%s)*$' % (TAG_MATCH, TAG_MATCH)
