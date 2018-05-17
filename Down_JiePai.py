#!/usr/bin/env python
# encoding: utf-8
'''
@author: Liujiaye
@contact: 15038556191@163.com
获取头条新闻街拍图片并按标题创建文件夹下载到本地
'''
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool

'''下载今日头条街拍美女图片'''


# 加载单个Ajax请求结果
def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autpload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        # 如果网页请求成功
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            # 获取标题
            title = item.get('title')
            # 获取图片列表
            images = item.get('image_list')
            for image in images:
                # 拼接高清图片地址
                real_image = 'https:' + (image.get('url')).replace('list', 'origin')
                yield {
                    'image': real_image,
                    'title': title
                }


def save_images(item):
    # 判断是否生成过同名文件
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        # 获取图片的二进制数据
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)

            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Faild to Save Image')


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_images(item)


# 起始页面
GROUP_START = 1
# 结束页面
GROUP_END = 3

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START - 1, GROUP_END + 1)])
    # 实现多线程下载
    pool.map(main, groups)
    pool.close()
    pool.join()
