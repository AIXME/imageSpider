# !/usr/bin/python
# encoding:utf-8
# 这个例子是去获取微博里的图片，例子爬取的微博是萌妹子吴倩：吴倩mine4ever
# 吴倩的微博id: 1900698023

# from selenium import webdriver

import ssl
import time
import requests
import urllib.request

import json
import os
import sys

request_params = {"ajwvr": "6", "domain": "100505", "domain_op": "100505", "feed_type": "0", "is_all": "1",
                  "is_tag": "0", "is_search": "0"}
# profile_request_params = {"profile_ftype":"1","is_all":"1"}

weibo_url = "https://m.weibo.cn/"
# WEIBO_SECOND_PROFILE_WEIBO 全部
# WEIBO_SECOND_PROFILE_WEIBO_ORI 原创
# WEIBO_SECOND_PROFILE_WEIBO_VIDEO 视频
# WEIBO_SECOND_PROFILE_WEIBO_ARTICAL 文章
# WEIBO_SECOND_PROFILE_WEIBO_WEIBO_SECOND_PROFILE_WEIBO_PIC 文章

cookie_save_file = "cookie.txt"#存cookie的文件名
cookie_update_time_file = "cookie_timestamp.txt"#存cookie时间戳的文件名
image_result_file = "image_result.md"#存图片结果的文件名

# 微博 id : https://weibo.com/u/{1900698023},u 后面的值；
# 有些明显是用的自定义域名，这个 ID 需要你自己去找了

user_id = input('请输入wb_id:')
weibo_type = 'WEIBO_SECOND_PROFILE_WEIBO_PIC'
containerid = '230413'+user_id
lfid = '230283'+user_id

_url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + containerid+'_-_'\
       +weibo_type+'&luicode=10000011&lfid=' + lfid

# cookie 去网页版获取，具体可以百度
cookie = 'MLOGIN=0; _T_WM=ec3cbb7caac2b6d765aa1c64e065ee7c; OUTFOX_SEARCH_USER_ID_NCOO=200622491.85643607; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302832101822767%26from%3Dpage_100306%26fid%3D2304132101822767_-_WEIBO_SECOND_PROFILE_PIC%26uicode%3D10000011'

# User-Agent需要根据每个人的电脑来修改
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'m.weibo.cn',
    'Pragma':'no-cache',
    'Referer':_url,
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'X-Requested-With':'XMLHttpRequest'
 }

# page_total = 1
cur_page = 1
n = 1
# This restores the same behavior as before.
# context = ssl._create_unverified_context()
# urllib.urlopen("https://no-valid-cert", context=context)


# 保存图片到本地
def save_image(img_src, id, pid, i):
    print(img_src)
    if not os.path.exists(str(user_id)):
        os.makedirs(str(user_id))
    _name = str(user_id) + '/' + str(id)+'_'+str(i)+'_' + str(pid) + '.jpg'
    print(_name)
    # urllib.request.urlretrieve(img_src, _name)
    if not os.path.exists(_name):
        r = requests.get(img_src)
        r.raise_for_status()
        # 使用with语句可以不用自己手动关闭已经打开的文件流
        with open(_name, "wb") as f:  # 开始写文件，wb代表写二进制文件
            f.write(r.content)
        print("爬取完成")
    else:
        print("文件已存在")


# 获取当前页的数据
def get_cur_page_weibo(_json, i):
    _cards = _json['data']['cards']
    _cardListInfo = _json['data']['cardlistInfo']
    global cur_page
    # page_total = _cardListInfo['total']  # 你要爬取的微博的页数
    cur_page = _cardListInfo['page']  # 当前微博页数
    print('当前页数：' + str(cur_page) + ';总页数' + str(page_total))
    # 打印微博
    for card in _cards:
        if card['card_type'] == 9:
            if card['mblog']['weibo_position'] == 1:
                if card['mblog']['pics']:
                    for x in range(len(card['mblog']['pics'])):
                        # 保存图片到本地
                        save_image(card['mblog']['pics'][x]['large']['url'], card['mblog']['created_at'], x, card['mblog']['mid'])
                        time.sleep(2)
                        # print(card['mblog'])


# 获取总页数
def get_total_page(_url):
    _response = requests.get(_url, headers=headers)
    print(_response.url)
    _html = _response.text
    __json = json.loads(_html)
    return __json['data']['cardlistInfo']['total']  # 你要爬取的微博的页数


# 总页数
page_total = int(get_total_page(_url))


# 遍历每一页
for i in range(1, page_total):
    headers['Cookie'] = cookie
    # print(_url)
    if i > 1:
        _url = _url+'&page_type=03&page='+str(i)
        print(_url)
    response = requests.get(_url, headers=headers)
    print(response.url)
    html = response.text
    _json = json.loads(html)
    get_cur_page_weibo(_json, i)
    # 休眠1秒
    time.sleep(1)
    if page_total > 10:
        if i % 10 == 0:
            # 每爬10页休眠10秒
            time.sleep(10)
