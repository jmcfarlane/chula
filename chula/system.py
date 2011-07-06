"""
Module to return operating system information

TODO: This module has not been tested on win32 at all
"""

# Python2.5 backports
from __future__ import with_statement

# Python imports
import os

LINUX = 'LINUX'
WIN32 = 'WIN32'
SUPPORTED = (LINUX, WIN32)

class System(object):
    def __init__(self):
        self.type = self.fetch_os()
        self.procs = getattr(self, 'fetch_procs_' + self.type.lower())()
        self.arch = self.fetch_arch()

    def fetch_arch(self):
        return os.uname()[4]

    def fetch_os(self):
        uname = os.uname()[0].upper()
        for name in SUPPORTED:
            if name == uname:
                return name

        return 'UNKONWN'

    def fetch_procs_linux(self):
        procs = 0
        with open('/proc/cpuinfo', 'r') as cpuinfo:
            for line in cpuinfo:
                if line.startswith('processor'):
                    procs += 1

        return procs

    def fetch_procs_win32(self):
        key = 'NUMBER_OF_PROCESSORS'
        if key in os.environ:
            return int(os.environ[key])

    def fetch_procs_unkonwn(self):
        return None
