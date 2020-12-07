import os
import etcd3
from dotenv import load_dotenv

MODE = 'MODE'
NUM_OF_WATCHABLES_PER_SESSION = 'NUM_OF_WATCHABLES_PER_SESSION'
MAX_USERS_PER_SESSION = 'MAX_USERS_PER_SESSION'
PAPERTRAIL_HOST = 'PAPERTRAIL_HOST'
PAPERTRAIL_PORT = 'PAPERTRAIL_PORT'

VARIABLES = [MODE, NUM_OF_WATCHABLES_PER_SESSION, MAX_USERS_PER_SESSION, PAPERTRAIL_HOST, PAPERTRAIL_PORT]

config = {}

def __config_via_etcd():
    ETCD_PORT = os.getenv('ETCD_PORT', 2379)
    try:
        etcd = etcd3.client(host=os.getenv('ETCD_HOST'), port=ETCD_PORT)
        for variable in VARIABLES:
            config[variable] = str(etcd.get(f'que-vemos:{variable}')[0], 'utf-8')
    except:
        __config_via_dotenv()

def __config_via_dotenv():
    load_dotenv()
    for variable in VARIABLES:
        config[variable] = str(os.getenv(variable))

def __verify_config(config):
    for var in VARIABLES:
        if config[var] == 'None':
            if var in (PAPERTRAIL_HOST, PAPERTRAIL_PORT):
                if config[MODE] == 'prod':
                    raise ConfigIncomplete(config)
            else:
                raise ConfigIncomplete(config)


class ConfigIncomplete(Exception):
    """ Exception raised when the app config is incomplete """
    def __init__(self, variables):
        self.message = f"One or more config variables are not defined {variables}"
        super().__init__(self.message)


if os.getenv('ETCD_HOST'):
    __config_via_etcd()
else:
    __config_via_dotenv()

__verify_config(config)
