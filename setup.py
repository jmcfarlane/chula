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

from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup
import os
import sys

import chula
from chula import error

# Check for dependencies
if 'install' in sys.argv:
    if sys.version_info < (2, 5):
        raise error.MissingDependencyError('Python-2.5 or higher')

# Attributes
download_url = 'http://rockfloat.com/chula/chula-%s.tar.gz' % chula.version
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

# Data files
data_files = []
for basedir, dirs, files in os.walk(chula.data_dir):
    if basedir.count(os.sep) > 0:
        files = [os.path.join(basedir, file) for file in files]
        basedir = os.path.join(chula.package_dir, basedir)
        data_files.append((basedir, files))

# Packages
packages = []
for basedir, dirs, files in os.walk(chula.package_dir):
    if '__init__.py' in files:
        packages.append(basedir.replace(os.sep, '.'))

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
# Credit: Django
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    author = 'John McFarlane',
    author_email = 'john.mcfarlane@rockfloat.com',
    classifiers = filter(None, classifiers.split("\n")),
    data_files = data_files,
    description = chula.__doc__.split('\n')[0],
    long_description = '\n'.join(chula.__doc__.split('\n')[2:]),
    download_url = download_url,
    license = 'GPL',
    maintainer = "John McFarlane",
    name = 'Chula',
    packages = packages,
    url='http://rockfloat.com/projects/chula/',
    version = chula.version
)
