# -*- coding: utf-8 -*-
import time
import json
from PIL import Image
import pyqrcode
import requests

def get_logininfo():
    """获取登录信息"""
    try:
        with open('./loginfo.dat', 'r', encoding='utf-8') as f:
            l = json.loads(f.read())
        return l
    except:
        return {}
loginfo = get_logininfo()

def loads(data: list):
    """将返回参数序列化为字典"""
    diction = {}
    for i in data:
        temp = i.split('=')
        diction[temp[0]] = temp[1]
    return diction


def getheader(name):
    """获取请求头"""
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    return header


def login_check():
    loginfo = get_logininfo()
    if loginfo == {}:
        return False
    """检查是否登录"""
    head = getheader('getQRcode')
    params = {'csrf': loginfo['bili_jct']}
    cookies = {'SESSDATA': loginfo['SESSDATA']}
    respond = requests.get('https://passport.bilibili.com/x/passport-login/web/cookie/info', headers=head, params=params, cookies=cookies).json()
    if respond['code'] == 0:
        # print(respond)
        if not respond['data']['refresh']:
            print('已登录')
            return True
        else:
            print('登录过期')
            return False
    else:
        print('未登录')
        return False


def getQRcode():
    """获取二维码"""
    head = getheader('getQRcode')
    respond = requests.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate', headers=head).json()
    # print(respond.text)
    if respond['code'] == 0:
        qrcodekey = respond['data']['qrcode_key']
        print(respond['data']['url'])
        qrcode = pyqrcode.create(respond['data']['url'])
        qrcode.png('qrcode.png', scale=8)
        print(qrcode.terminal(quiet_zone=1))
        Image.open('qrcode.png').show()
        return True
    else:
        return False


def QRcodeLogin():
    """二维码登录"""
    if not login_check():
        global qrcodekey
        head = getheader('getQRcode')
        respond = requests.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate', headers=head).json()
        # print(respond.text)
        if respond['code'] == 0:
            qrcodekey = respond['data']['qrcode_key']
            print(respond['data']['url'])
            qrcode = pyqrcode.create(respond['data']['url'])
            qrcode.png('qrcode.png', scale=8)
            print(qrcode.terminal(quiet_zone=1))
            Image.open('qrcode.png').show()
            print('请扫描二维码登录')
        while True:
            log_respond = requests.get('https://passport.bilibili.com/x/passport-login/web/qrcode/poll',
                                       params={'qrcode_key': qrcodekey}, headers=head).json()
            if log_respond['code'] == 0:
                if log_respond['data']['code'] == 0:
                    print('登录成功')
                    return loads(log_respond['data']['url'].split('?')[1].split('&'))
                    # break
                else:
                    if log_respond['data']['code'] == 86090:
                        print('请点击确认登录')
                        time.sleep(2)
                    elif log_respond['data']['code'] == 86101:
                        print('请扫码')
                        time.sleep(2)
                    elif log_respond['data']['code'] == 86038:
                        print('二维码已过期')
                        break
                    else:
                        print(log_respond['data']['message'])
                        break
    else:
        print('已登录,无需二维码登录！')
        return get_logininfo()
def login():
    a = QRcodeLogin()
    with open('./loginfo.dat', 'w', encoding='utf-8') as f:
        f.write(json.dumps(a))
    return a

def get_userinfo(uid):
    head = getheader('getQRcode')
    param = {'vmid': uid}
    cookie = {'SESSDATA': loginfo['SESSDATA']}
    respond = requests.get('https://api.bilibili.com/x/relation/stat', headers=head, params=param, cookies=cookie).json()
    if respond['code'] == 0:
        print(respond)
        return respond['data']['follower']
    else:
        return None

def is_living(rid):
    url = 'https://api.live.bilibili.com/room/v1/Room/get_info'
    params = {'room_id': rid}
    head = getheader('getQRcode')
    resp = requests.get(url, headers=head, params=params).json()['data']
    if resp['live_status'] == 1:
        stat = time.strftime('%m%d-%H:%M:%S', time.localtime(time.time()))+'---直播中'
        print('{:=^50}'.format(stat))
        return True
    else:
        stat = time.strftime('%m%d-%H:%M:%S', time.localtime(time.time()))+'---未直播'
        print('{:=^50}'.format(stat))

        return False

# login()