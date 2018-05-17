#!/usr/bin/env python
# encoding: utf-8
'''
通过selenium模拟浏览器操作获取淘宝商品信息
@author: Liujiaye
@contact: 15038556191@163.com
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq

options_chrome = webdriver.ChromeOptions()
options_chrome.binary_location = r"G:\UseFor\Chrome\chrome.exe"  # 本地chrome.exe地址
options_chrome.add_argument('--headless')  # 无界面模式
browser = webdriver.Chrome(chrome_options=options_chrome)
wait = WebDriverWait(browser, 10)
KEYWORD = 'iPad'  # 关键词
MAX_PAGE = 2  # 页数


# browser.get('https://www.baidu.com/?tn=92726165_s_hao_pg')

def index_page(page):
    '''
    爬取索引页
    :param page: 页码
    '''
    print('正在爬取第', page, '页')
    try:
        # 组建链接
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        # 如果页码>1 进行跳页操作
        if page > 1:
            # 获取页码输入框
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input'))
            )
            # 获取跳选指定页面按钮
            sumbit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit'))
            )
            # 清空输入框并输入page
            input.clear()
            input.send_keys(page)
            # 点击跳转
            sumbit.click()
        # 确认是否跳转到对应页码
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page))
        )
        # 确认商品都加载出来
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item'))
        )
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    '''
    获取页面商品信息
    :return:
    '''
    # 获取页面源码
    html = browser.page_source
    doc = pq(html)
    # 所有商品集合
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        # 此处可加入存储数据库方法
        # save_to_Mysql/MongDB()


def main():
    '''
    遍历每一页
    '''
    for i in range(1, MAX_PAGE + 1):
        index_page(i)


if __name__ == '__main__':
    main()
