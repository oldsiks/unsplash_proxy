

import redis
from settings import REDIS_INI, REDIS_KEY_NAME

class RedisConfig:

    rc = redis.Redis(
        host=REDIS_INI['host'],
        port=REDIS_INI['port'],
        decode_responses=REDIS_INI['decode_responses'],
        db=REDIS_INI['db']
    )
    @staticmethod
    def cache_keep(flag: bool):
        if flag:
            pass
        else:
            RedisConfig.rc.delete(REDIS_KEY_NAME['finger'], REDIS_KEY_NAME['link'])

if __name__ == '__main__':
    rc = RedisConfig.rc
    print(rc.lpop('heheda'))



