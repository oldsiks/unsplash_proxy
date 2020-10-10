

import os
import re
import time
import requests
import hashlib
from random import randint, choice
from DBConfig import RedisConfig
from settings import HEADERS, PATH, KEY_DIR, SQL, console_logger, root_logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
img_type = re.compile(r'fm=(.*?)&')

class DownImage(object):

    def __init__(self):
        self.rc = RedisConfig.rc
        self.headers = HEADERS
        self.hash_object = HashLink

    def get_link(self):
        return self.rc.lpop('unsplash_link')

    def sadd_finger(self, finger):
        return self.rc.sadd('unsplash_finger', finger)

    def judge(self, finger):
        return self.rc.sismember('unsplash_finger', finger)

    def get_image_type(self, url: str):
        return img_type.search(url).group(1)

    def get_proxy(self):
        proxy_list = self.rc.lrange('proxy', 0, -1)
        return proxy_list

    def download(self, image_path, sql_path, link, key_type, proxy):
        image_type = self.get_image_type(link)
        finger = self.hash_object().creat_finger(link)
        file_name = finger + '.' + image_type
        file_path = os.path.join(image_path, file_name)
        tries_num = 3
        sleep_time = 1
        proxies = {'http': proxy}

        if self.judge(finger) != 1:
            for i in range(tries_num):
                try:
                    image = requests.get(url=link, headers=self.headers, timeout=120, proxies=proxies, verify=False)
                    with open(file_path, 'wb') as f:
                        f.write(image.content)
                        f.flush()
                    self.sadd_finger(finger)
                    with open(sql_path, 'a', encoding='utf-8') as fq:
                        fq.write(SQL.format(link, KEY_DIR[key_type], file_name, key_type))
                    time.sleep(randint(2, 5)/10)
                    console_logger.info(f'已抓取图片{file_name}')
                    return
                except Exception as exc:
                    if i < 2:
                        root_logger.error(f'{exc} ------  在{sleep_time}秒后，重新发起第{i}次请求')
                        time.sleep(sleep_time)
                    if i == 2:
                        self.rc.rpush('links', str((link, key_type)))
                        root_logger.info(f'已将{link}重新加入队列')
                    sleep_time += 1

    def run(self):
        lpop_times = 0
        while True:
            proxy_list = self.get_proxy()
            proxy = choice(proxy_list)
            parameter = self.get_link()
            if parameter:
                link, key_type = eval(parameter)
                image_path = PATH + '/image/{0}'.format(KEY_DIR[key_type])
                sql_file = PATH + '/sql_file'
                if not os.path.exists(image_path):
                    os.makedirs(image_path)
                if not os.path.exists(sql_file):
                    os.makedirs(sql_file)
                sql_path = os.path.join(sql_file, f'{KEY_DIR[key_type]}.sql')
                self.download(image_path=image_path, sql_path=sql_path, link=link, key_type=key_type, proxy=proxy)
            else:
                time.sleep(5)
                if lpop_times < 10:
                    root_logger.error('连续三次未从link池中获取url，终止程序')
                    break

class HashLink:

    def __init__(self):
        self.ham5 = hashlib.md5()

    def creat_finger(self, url):
        self.ham5.update(url.encode(encoding='utf-8'))
        return self.ham5.hexdigest()