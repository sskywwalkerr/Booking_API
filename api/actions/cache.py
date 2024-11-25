from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis


def init_cache():
    redis_client = Redis(host='localhost', port=6379, db=0)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")