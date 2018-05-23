#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Liujiaye
@contact: 15038556191@163.com
抓取猫眼电影TOP100的电影信息
'''
import json
import re
import time

import requests
from requests.exceptions import RequestException


def get_one_page(url):
    '''
    获取每页源码
    :param url: 每页网址
    '''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
        }
        response = requests.get(url, headers=headers)
        # 判断响应状态码
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    '''
    :param html: 每页源码
    '''
    # 正则表达式匹配
    parm = re.compile(
        '^<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S
    )
    #匹配网页
    items = re.findall(parm, html)
    # 重新排版
    for item in items:
        yield {
            '排名': item[0],
            '图片': item[1],
            '名称': item[2].strip(),
            '主演': item[3].strip()[3:] if len(item[3]) > 3 else '',
            '上映时间': item[4].strip()[5:] if len(item[4]) > 5 else '',
            '评分': item[5].strip() + item[6].strip(),
        }


def write_to_txt(item):
    '''
    保存到本地
    :param item: 电影信息
    '''
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4' + str(offset)
    html = get_one_page(url)
    #获取一页内所有电影信息
    for item in parse_one_page(html):
        write_to_txt(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        # 休眠2秒,防止爬取过快
        time.sleep(2)
