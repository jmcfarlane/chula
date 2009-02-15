"""
Chula fastcgi adapter
"""

from chula.www.adapters.wsgi.adapter import wsgi

# Thanks to fcgi.py we can serve fastcgi apps using wsgi
fcgi = wsgi
