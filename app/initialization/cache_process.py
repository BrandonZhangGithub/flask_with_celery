from flask_caching import Cache
from . import app
from configs.sysconf import (
    REDIS_CONFIG,
    CACHING_TIMEOUT,
    CACHING_KEY_REFIX
)

config = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": CACHING_TIMEOUT,
    "CACHE_KEY_PREFIX": CACHING_KEY_REFIX,
    "CACHE_REDIS_HOST": REDIS_CONFIG['host'],
    "CACHE_REDIS_PORT": REDIS_CONFIG['port'],
    "CACHE_REDIS_PASSWORD": REDIS_CONFIG['REDIS_PASSWD'],
}

app.config.from_mapping(config)
cache = Cache(app)