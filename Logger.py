# coding: utf-8
import logging


class Logger(object):

    def __init__(self, name='logger', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler('%s.log' % name, 'w')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

log = Logger(name='IOTMain', level=logging.DEBUG)

if __name__ == '__main__':
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
