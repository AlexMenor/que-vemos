import os
import etcd3
from dotenv import load_dotenv

class Config:
    def __init__(self):
        if os.getenv('ETCD_HOST'):
            self.__config_via_etcd()
        else:
            self.__config_via_dotenv()

        self.__verify_config()

    def __config_via_etcd(self):
        ETCD_PORT = os.getenv('ETCD_PORT', 2379)
        try:
            etcd = etcd3.client(host=os.getenv('ETCD_HOST'), port=ETCD_PORT)
        except:
            self.__config_via_dotenv()
            return

        self.mode = etcd.get('que-vemos:MODE') if etcd.get('que-vemos:MODE') else 'dev'
        self.num_of_watchables_per_session = etcd.get('que-vemos:NUM_OF_WATCHABLES_PER_SESSION')
        self.max_users_per_session = etcd.get('que-vemos:MAX_USERS_PER_SESSION')
        self.papertrail_host = etcd.get('que-vemos:PAPERTRAIL_HOST')
        self.papertrail_port = etcd.get('que-vemos:PAPERTRAIL_PORT')

    def __config_via_dotenv(self):
        load_dotenv()
        self.mode = os.getenv('MODE', 'dev')
        self.num_of_watchables_per_session = os.getenv('NUM_OF_WATCHABLES_PER_SESSION')
        self.max_users_per_session = os.getenv('MAX_USERS_PER_SESSION')
        self.papertrail_host = os.getenv('PAPERTRAIL_HOST')
        self.papertrail_port = os.getenv('PAPERTRAIL_PORT')

    def __verify_config(self):
        variables = self.__dict__

        for var_name in variables:
            if variables[var_name] is None:
                if var_name == 'papertrail_host' or var_name == 'papertrail_port':
                    if variables['mode'] == 'prod':
                        raise ConfigIncomplete(variables)
                else:
                    raise ConfigIncomplete(variables)


class ConfigIncomplete(Exception):
    """ Exception raised when the app config is incomplete """
    def __init__(self, variables):
        self.message = f"One or more config variables are not defined {variables}"
        super().__init__(self.message)


config = Config()
