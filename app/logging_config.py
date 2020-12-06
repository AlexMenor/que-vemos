import logging
import socket
from logging.handlers import SysLogHandler

class ContextFilter(logging.Filter):
    hostname = socket.gethostname()
    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


syslog = SysLogHandler(address=('logsN.papertrailapp.com', 00000))

syslog.addFilter(ContextFilter())

format = '%(asctime)s %(hostname)s que-vemos: %(message)s'

formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)

