"""Chula logger class"""

import logging
from logging.handlers import RotatingFileHandler

from chula.config import Config
from chula.singleton import singleton

ROOT = 'chula'

@singleton
class Logger(object):
    def __init__(self, config=None):
        if config is None:
            config = Config()

        # Create file handler for WARNING and above
        fmt = ('%(asctime)s,'
               '%(levelname)s,'
               'pid:%(process)d,'
               '%(name)s,'
               '%(filename)s:%(lineno)d,'
               '%(message)s'
              )
        fh = RotatingFileHandler(config.log, maxBytes=104857600, backupCount=5)
        fh.setLevel(logging.WARNING)
        fh.setFormatter(logging.Formatter(fmt))

        # Create console handler for DEBUG and above (stderr)
        fmt = ('%(levelname)-9s'
               '%(name)-35s'
               '%(filename)-15s'
               '%(lineno)-5d'
               '%(message)s'
              )
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter(fmt))

        # Create a logger instance.  NOTE: the level set in the logger
        # determines which severity of messages it will pass to it's
        # handlers.  We want to send everything to the handlers and
        # let them decide what to do.
        logger = logging.getLogger('')
        logger.setLevel(logging.DEBUG)

        # Add the handlers
        logger.addHandler(ch)
        logger.addHandler(fh)

    def logger(self, name=ROOT):
        if not name.startswith(ROOT):
            name = '%s.%s' % (ROOT, name)

        return logging.getLogger(name)

if __name__ == '__main__':
    from chula import config
    config = config.Config()

    logger = Logger(config).logger()
    foo = Logger(config).logger('foo')
    bar = Logger(config).logger('chula.bar')

    logger.critical('critical msg')
    logger.debug('debug msg')
    logger.error('error msg')
    logger.info('info msg')
    logger.warning('warning msg')

    foo.warning('warning msg')
    bar.warning('warning msg')
    foo.info('info msg')
