import redis
from utilities.settings import settings


def get_redis_client():
    try:
        redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
        return redis_client
    except redis.exceptions.ConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")
        return None
