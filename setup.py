#setup.py - Chula
#
#Copyright (C) 2010 John McFarlane <john.mcfarlane@rockfloat.com>
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

from setuptools import setup, find_packages
import os
import sys

import chula
from chula import error

# Check for dependencies
if 'install' in sys.argv:
    if sys.version_info < (2, 6):
        raise error.MissingDependencyError('Python-2.6 or higher')

# Attributes
AUTHOR = 'John McFarlane'
CLASSIFIERS = """
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Operating System :: OS Independent
Programming Language :: Python
Topic :: Database
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Software Development
Topic :: Software Development :: Libraries :: Python Modules
"""
EMAIL = 'john.mcfarlane@rockfloat.com'
INSTALL_REQUIRES = []
LICENSE = 'GPL'
NAME = 'Chula'
TESTS = 'tests'
URL = 'http://chula.rockfloat.com'
URL_ = URL + '/downloads/Chula-%s.tar.gz' % chula.version
ZIP_SAFE = True

setup(
    author = AUTHOR,
    author_email = EMAIL,
    classifiers = [c for c in CLASSIFIERS.split('\n') if c],
    description = chula.__doc__.split('\n')[0],
    download_url = URL_,
    install_requires = INSTALL_REQUIRES,
    license = LICENSE,
    long_description = '\n'.join(chula.__doc__.split('\n')[2:]),
    name = NAME,
    packages = find_packages(),
    test_suite = TESTS,
    url = URL,
    version = chula.version,
    zip_safe = ZIP_SAFE
)
