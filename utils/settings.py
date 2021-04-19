import configparser
import stock_management
import redis as redis


def get_all_env_variables():
    config_variables = configparser.ConfigParser()
    config_variables.read_file(open(r"stock_management/configuration.cfg"))
    return config_variables


config_variables = get_all_env_variables()

REDIS_HOST = config_variables.get("Redis-Cred", "host")
REDIS_PORT = int(config_variables.get("Redis-Cred", "port"))
REDIS_PASSWORD = None if config_variables.get("Redis-Cred", "password") == 'None' else config_variables.get(
    "Redis-Cred", "password")
REDIS_SSL = bool(int(config_variables.get("Redis-Cred", "ssl")))
REDIS_INSTANCE = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, ssl=REDIS_SSL, password=REDIS_PASSWORD)
