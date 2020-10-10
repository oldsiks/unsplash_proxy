
import time
import requests
from DBConfig import RedisConfig
from settings import PROXY


class ProxyPool(object):

    def __init__(self):
        self.url = PROXY['url']
        self.appcode = PROXY['appcode']
        self.rc = RedisConfig.rc

    def get_api_to_redis(self):
        headers = {'Authorization': f'appcode {self.appcode}'}
        response = requests.get(url=self.url, headers=headers).json()
        proxy_list = response['result']
        for p in proxy_list:
            self.rc.lpush('proxy', str(p))

    def run(self):
        while True:
            if self.rc.llen('proxy') <= 10:
                self.get_api_to_redis()
            time.sleep(60)







