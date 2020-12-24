import pytest
from ...config.config import __verify_config, NUM_OF_WATCHABLES_PER_SESSION, MAX_USERS_PER_SESSION, MODE, PAPERTRAIL_PORT, PAPERTRAIL_HOST, ConfigIncomplete, REDIS_URL


@pytest.fixture
def positive_config_dev():
    return {
       NUM_OF_WATCHABLES_PER_SESSION: '10',
        MAX_USERS_PER_SESSION: '8',
        MODE: 'dev',
        PAPERTRAIL_PORT: 'None',
        PAPERTRAIL_HOST: 'None',
        REDIS_URL: 'None'
    }

@pytest.fixture
def positive_config_prod():
    return {
        NUM_OF_WATCHABLES_PER_SESSION: '10',
        MAX_USERS_PER_SESSION: '8',
        MODE: 'prod',
        PAPERTRAIL_PORT: '4444',
        PAPERTRAIL_HOST: 'localhost',
        REDIS_URL: 'redis://localhost'
    }

@pytest.fixture
def negative_config_dev():
    return {
        NUM_OF_WATCHABLES_PER_SESSION: 'None',
        MAX_USERS_PER_SESSION: '8',
        MODE: 'dev',
        PAPERTRAIL_PORT: 'None',
        PAPERTRAIL_HOST: 'None',
        REDIS_URL: 'None'
    }

@pytest.fixture
def negative_config_prod():
    return {
        NUM_OF_WATCHABLES_PER_SESSION: '10',
        MAX_USERS_PER_SESSION: '8',
        MODE: 'prod',
        PAPERTRAIL_PORT: '4444',
        PAPERTRAIL_HOST: 'localhost',
        REDIS_URL: 'None'
    }

def test_verify_config_positive_dev(positive_config_dev):
    __verify_config(positive_config_dev)

def test_verify_config_positive_prod(positive_config_prod):
    __verify_config(positive_config_prod)

def test_verify_config_negative_dev(negative_config_dev):
    with pytest.raises(ConfigIncomplete):
        __verify_config(negative_config_dev)

def test_verify_config_negative_prod(negative_config_prod):
    with pytest.raises(ConfigIncomplete):
        __verify_config(negative_config_prod)
