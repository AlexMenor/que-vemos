import logging
import socket
import sys

from logging.handlers import SysLogHandler

from .config import config, MODE, PAPERTRAIL_PORT, PAPERTRAIL_HOST

class ContextFilter(logging.Filter):
    hostname = socket.gethostname()
    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


if config[MODE] == 'prod':
    handler = SysLogHandler(address=(config[PAPERTRAIL_HOST], int(config[PAPERTRAIL_PORT])))
else:
    handler = logging.StreamHandler(sys.stdout)

handler.addFilter(ContextFilter())
format = '%(asctime)s %(hostname)s que-vemos: %(message)s'

formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')

handler.setFormatter(formatter)

