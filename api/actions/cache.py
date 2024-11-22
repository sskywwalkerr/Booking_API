# import redis
# import time
# from utilities.settings import settings
#
#
# class RedisCache:
#     def __init__(self):
#         self.redis = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
#
#     def set_user(self, username, user_id, expiration_time=3600): # кэшируем на 1 час
#         try:
#             self.redis.set(f"user:{username}", user_id, ex=expiration_time)
#             return True
#         except Exception as e:
#             print(f"Ошибка кэширования пользователя в Redis: {e}")
#             return False

import redis
from utilities.settings import settings

def get_redis_client():
    """Создает и возвращает клиент Redis."""
    try:
        redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
        return redis_client
    except redis.exceptions.ConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")
        #Здесь можно добавить более robust обработку ошибок, например,  возврат None или raise Exception
        return None


#Пример использования:
redis_client = get_redis_client()
if redis_client:
    #Ваш код работы с Redis
    redis_client.set("mykey", "myvalue")
    print(redis_client.get("mykey"))
else:
    print("Не удалось подключиться к Redis.")