# -*- coding: utf-8 -*- 
"""
@Time        : 2020/5/1 10:30 
@Author      : tmooming
@File        : test.py.py 
@Description : TODO
"""
import json

import requests
import sys
import time

word_url = 'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word={}'
COOKIES = 'CHKFORREG=74223646f34140a158db712ecfdb4cee; BAIDUID=7C4422DE481F571C7E041263530CC49A:FG=1; BIDUPSID=7C4422DE481F571C7E041263530CC49A; PSTM=1571639074; MCITY=-315%3A; BDUSS=1A5MktCSnRQeExmRjAzWE9vVU56QXlVd29McmVqcUFaa05pVUlGYzVDSFZyc1JlRVFBQUFBJCQAAAAAAAAAAAEAAAB1PMDJsKLLubbZxaPI4gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANUhnV7VIZ1eb; ZD_ENTRY=empty; H_PS_PSSID=31351_1461_31169_21092_31253_31423_31341_31464_30823_26350_31164_31473; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=3; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1588299798; bdindexid=32rk4ts1k7ibl1nor068lv17o0; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1588300131; RT="z=1&dm=baidu.com&si=9nnqsci8esv&ss=k9nkoukr&sl=6&tt=aja&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"'


def decrypt(t, e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n) / 2)
    start = n[ln:]
    end = n[:ln]
    for j, k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    return ''.join(result)


def get_index_home(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'Cookie': COOKIES
    }
    resp = requests.get(word_url.format(keyword), headers=headers)
    j = resp.json()
    uniqid = j.get('data').get('uniqid')
    return get_ptbk(uniqid)


def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={}'
    ptbk_headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': COOKIES,
        'DNT': '1',
        'Host': '百度指数',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': '百度指数',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    resp = requests.get(url.format(uniqid), headers=ptbk_headers)
    if resp.status_code != 200:
        print('获取uniqid失败')
        sys.exit(1)
    return resp.json().get('data')


def get_index_data(keyword, start='2011-01-03', end='2019-08-05'):
    url = f'http://index.baidu.com/api/SearchApi/index?word={keyword}&area=0&startDate={start}&endDate={end}'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': COOKIES,
        'DNT': '1',
        'Host': 'index.baidu.com',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print('获取指数失败')
        sys.exit(1)
    print(resp.text)
    number_data = json.loads(resp.text)['data']
    data = json.loads(resp.text)['data']['userIndexes'][0]
    uniqid = json.loads(resp.text)['data']['uniqid']
    ptbk = get_index_home(uniqid)
    while ptbk is None or ptbk == '':
        ptbk = get_index_home(uniqid)
    all_data = data['all']['data']
    result = decrypt(ptbk, all_data)
    result = result.split(',')
    print(result)


if __name__ == '__main__':
    get_index_data('酷安')