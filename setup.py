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

"""Chula is a lightweight web framework for mod_python"""

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

from distutils.core import setup

import chula
version = chula.version

setup(author='John McFarlane',
      author_email='john.mcfarlane@rockfloat.com',
      classifiers=filter(None, classifiers.split("\n")),
      description=__doc__.split("\n")[0],
      download_url = "http://rockfloat.com/chula/chula-%s.tar.gz" % version,
      license='GPL',
      maintainer="John McFarlane",
      name='chula',
      package_dir={'chula':'chula'},
      packages=['chula', 'chula.test', 'chula.www']
      platforms = ["any"],
      url='http://rockfloat.com/projects/chula/',
      version=version)
