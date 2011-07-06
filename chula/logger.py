"""Chula logger class"""

# Python imports
import logging
from logging.handlers import RotatingFileHandler

# Project imports
from chula.config import Config
from chula.singleton import singleton

ROOT = 'chula'

class Logger(object):
    def __init__(self, config=None):
        if config is None:
            config = Config()

        # Create a logger instance.  NOTE: the level set in the logger
        # determines which severity of messages it will pass to it's
        # handlers.  We want to send everything to the handlers and
        # let them decide what to do (aka this must pass everything
        # along).
        logger = logging.getLogger('')
        logger.setLevel(logging.DEBUG)

        # Create file handler for WARNING and above
        if not config.log is None:
            fmt = ('%(asctime)s, '
                   '%(clientip)s, '
                   '%(levelname)s, '
                   'pid:%(process)d, '
                   '%(name)s, '
                   '%(filename)s:%(lineno)d, '
                   '%(message)s'
                  )
            fh = RotatingFileHandler(config.log,
                                     maxBytes=104857600,
                                     backupCount=5)
            fh.addFilter(logging.Filter(ROOT))
            fh.setLevel(config.log_level)
            fh.setFormatter(logging.Formatter(fmt))
            logger.addHandler(fh)

        # Create file handler for DEBUG and above
        if config.debug and config.log:
            fmt = ('%(levelname)-9s'
                   '%(name)-35s'
                   '%(filename)-15s'
                   '%(lineno)-5d'
                   '%(message)s'
                  )
            fh = RotatingFileHandler(config.log + '.debug',
                                     maxBytes=104857600,
                                     backupCount=5)
            fh.setLevel(config.log_level - 20)
            fh.setFormatter(logging.Formatter(fmt))
            logger.addHandler(fh)

    def logger(self, name=ROOT):
        if not name.startswith(ROOT):
            name = '%s.%s' % (ROOT, name)

        return logging.getLogger(name)

# Make the Logger a singleton.  Switch to a class decorator when
# python-2.5 support is no longer needed
Logger = singleton(Logger)

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
