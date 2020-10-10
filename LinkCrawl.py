

import json
import time
import random
import requests
from DBConfig import RedisConfig
from settings import INI_LINK, HEADERS, INIT_KEY, CACH_KEEP, console_logger, root_logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

RedisConfig.cache_keep(CACH_KEEP)

class DownLink(object):

    def __init__(self):
        self.rc = RedisConfig.rc
        self.headers = HEADERS
        self.key_list = INIT_KEY
        self.link = INI_LINK

    def get_link(self, page, keyword, key_type, proxy):

        params = {
            'query': keyword,
            'per_page': '20',
            'page': page,
        }
        proxies = {'http': proxy}
        resp = requests.get(url=self.link, params=params, headers=self.headers, proxies=proxies, verify=False)
        if resp.status_code != 403:
            root_logger.info(resp.status_code)
            content_json = json.loads(resp.text)
            if 'errors' not in content_json:
                try:
                    content_num = len(content_json['results'])
                    if content_num != 0:
                        for block in content_json['results']:
                            link = block['urls']['regular']
                            self.rc.rpush('unsplash_link', str((link, key_type)))
                        console_logger.info('已经向redis中添加{0}类，第{1}页！'.format(keyword, page))
                        self.rc.lpush('mark', str(()))
                        return 0
                    else:
                        return 1
                except BaseException as e:
                    console_logger.error(e)
                    root_logger.error(content_json)
            else:
                return 1
        else:
            return 2

    def get_crawled_mark(self):
        return self.rc.lrange('mark', 0, -1)

    def get_proxy(self):
        proxy_list = self.rc.lrange('proxy', 0, -1)
        return proxy_list


    def run(self):
        load_mark = self.get_crawled_mark()
        for keyword, key_type in self.key_list.items():
            page = 1
            loop_times = 1
            while True:
                proxy_list = self.get_proxy()
                proxy = random.choice(proxy_list)
                mark_key = str((keyword, page))
                if mark_key not in load_mark:
                    try:
                        flag = self.get_link(page=page, keyword=keyword, key_type=key_type, proxy=proxy)
                        time.sleep(3)
                        page += 1
                        if flag == 0:
                            break
                        elif flag == 2:
                            self.rc.lrem('proxy', 0, proxy)
                    except BaseException as exc:
                        root_logger.error(f"关键字：{keyword}，第{page}页，第{loop_times}次发生错误{exc}")
                        root_logger.exception(exc)
                        time.sleep(10)
                else:
                    page += 1
                    console_logger.info(f'{mark_key}已载入····')
                    pass

