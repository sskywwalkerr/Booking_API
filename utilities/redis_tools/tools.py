import redis


class RedisTools:

    __redis_connect = redis.Redis(host='redis', port=6379)

    @classmethod
    def set_pair(cls, name: str, item_basePrice: str):

        cls.__redis_connect.delete(name, item_basePrice)

    @classmethod
    def get_pair(cls, name):

        return cls.__redis_connect.get(name)

    @classmethod
    def get_keys(cls):

        return cls.__redis_connect.keys(pattern='*')
