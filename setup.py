#setup.py - Chula
#
#Copyright (C) 2007 John McFarlane <john.mcfarlane@rockfloat.com>
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

classifiers = """
Development Status :: 3 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: Database
Topic :: Software Development
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
"""

import sys

from distutils.core import setup

import chula

# Check for dependencies
if 'install' in sys.argv:
    from chula import error

    if sys.version_info < (2, 5):
        raise error.MissingDependencyError('Python-2.5 or higher')

    # Simplejson
    try:
        import simplejson
    except:
        raise error.MissingDependencyError('Simplejson')
        
    # Psycopg
    try:
        import psycopg2
    except:
        raise error.MissingDependencyError('Psycopg2')

# Data files
sql_session = ['sql/session/reload', 'sql/session/schema.sql']
sql_test = ['sql/test/reload', 'sql/test/schema.sql']

version = chula.version
setup(author='John McFarlane',
      author_email='john.mcfarlane@rockfloat.com',
      classifiers=filter(None, classifiers.split("\n")),
      data_files=[('share/chula/sql/session', sql_session),
                  ('share/chula/sql/test', sql_test)],
      description=chula.__doc__.split('\n')[0],
      long_description='\n'.join(chula.__doc__.split('\n')[2:]),
      download_url = "http://rockfloat.com/chula/chula-%s.tar.gz" % version,
      license='GPL',
      maintainer="John McFarlane",
      name='chula',
      package_dir={'chula':'chula'},
      packages=['chula', 'chula.test', 'chula.www'],
      platforms = ["any"],
      url='http://rockfloat.com/projects/chula/',
      version=version)

