
"""
    @Author  : Eric Liu
    @Date    : 2020.10.09_
    @function: 爬虫请求参数，初始url，User_Agent，redis，数据库相关参数的配置
"""

import logging.config
from fake_useragent import UserAgent

ua = UserAgent(path='fake_useragent_0.1.11.json')  # User_Agent配置

INI_LINK = 'https://unsplash.com/napi/search/photos?'  # 初始URL，当接口发生变化在此修改
INIT_KEY = {'animals': 1, 'food': 2, 'drink': 2, 'bar': 3, 'DJ': 3, 'nature': 4, 'travel': 4,
            'urban': 4, 'building': 4, 'hotel': 4, 'outdoor': 4, 'snow': 4, 'china': 4, 'Japan': 4,
            'road': 4, 'rain': 4, 'sport': 5, 'motorbike': 9, 'art': 9, 'music': 9, 'bed': 9, 'book': 9,
            'library': 9, 'rose': 9, 'handwriting': 9, 'paper': 9}  # 待爬取关键字
KEY_DIR = {1: 'pet', 2: 'desserts', 3: 'nightclub', 4: 'tour', 5: 'sport', 6: 'food', 7: 'game', 8: 'coser', 9: 'life'}

HEADERS = {
        'authority': 'api.500px.com', 'method': 'GET', 'scheme': 'https', 'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'User-Agent': ua.random,
        'cache-control': 'no-cache', 'origin': 'https://500px.com', 'referer': 'https://500px.com/'
}

CACH_KEEP = False  # 是否持续化数据中的key
REDIS_INI = {'host': '127.0.0.1', 'port': 6379, 'decode_responses': True, 'db': 1}
REDIS_KEY_NAME = {'finger': 'unsplash_finger', 'link': 'unsplash_link'}

PATH = '/data/server/unsplash'
SQL = 'insert into disposition_photo (`origin_url`, `url`, `type`) values ("{0}", "https://cdn-static.real-dating.cn/server/disposition-photo/{1}/{2}", {3});\n'

logging.config.fileConfig('logging.conf')
console_logger = logging.getLogger('simple')
root_logger = logging.getLogger('root')

PROXY = {'url': 'http://zip.market.alicloudapi.com/devtoolservice/ipagency?foreigntype=0&protocol=0', 'appcode': '6b385e6b96c042a6adaf46ff51595b54'}
