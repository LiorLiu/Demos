#!/usr/bin/env python
# encoding: utf-8
'''
@author: Liujiaye
@contact: 15038556191@163.com
利用IFTTT实时获取比特币价格，以及比特币价格紧急通知 按需修改BITCOIN_PRICE_THRESHOLD
'''
import requests
import time
from datetime import datetime

coinmarketcap_api_url = 'https://api.coinmarketcap.com/v2/ticker/?convert=BTC&limit=10'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{0}/with/key/{your-IFTTT-key}'
BITCOIN_PRICE_THRESHOLD = 10000  # 比特币价格(紧急通知)


# 获取比特币价格
def get_lastest_bitcoin_price():
    response = requests.get(coinmarketcap_api_url)
    response_json = response.json()
    # 获取比特币价格
    BTC_USD_price = response_json['data']['1']['quotes']['USD']['price']
    return float(BTC_USD_price)


# 发送消息
def post_ifttt_webhook(event, value):
    data = {'value1': value}
    # 替换请求地址
    ifttt_webhook_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_webhook_url, json=data)


# 比特币消息排版
def format_bitcoin_history(bitcion_history):
    rows = []
    for biction_price in bitcion_history:
        data = biction_price['data'].strftime('%d.%m.%Y %H:%M')
        price = biction_price['price']
        row = '{0}:$<b>{1}</b>'.format(data, price)
        rows.append(row)
    return '<br>'.join(rows)


def main():
    # 用来存储比特币价格
    bitcion_history = []
    while True:
        price = get_lastest_bitcoin_price()
        data = datetime.now()
        bitcion_history.append({'data': data, 'price': price})

        # 当价格低与BITCOIN_PRICE_THRESHOLD发送紧急通知
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # 按时发送比特币信息
        if len(bitcion_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcion_history))

            bitcion_history = []

        # 休眠5分钟，防止过于频繁获取信息
        time.sleep(5 * 60)


if __name__ == '__main__':
    main()
