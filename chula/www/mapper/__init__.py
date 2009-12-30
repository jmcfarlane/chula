"""
Chula URL mapping package
"""

import copy

import chula
from chula import collection, error

DEFAULT_MODULE = 'home'
DEFAULT_METHOD = 'index'

# Include supported mappers
from chula.www.mapper.classpath import ClassPathMapper
from chula.www.mapper.regex import RegexMapper
