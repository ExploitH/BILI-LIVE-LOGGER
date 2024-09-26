import json
import time

import requests
import websockets
import asyncio
import callback
import login
import proto
from multiprocessing import Process, freeze_support

##################################请配置#####################################
# 房间号
roomid = 00000000
#没错，只有这个awa



loginfo = login.login()
Myuid = int(loginfo['DedeUserID'])
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


def getcookie():
    url = f'https://api.bilibili.com/x/frontend/finger/spi'
    s = requests.session()
    resp = s.get(url=url, headers=header, cookies=loginfo)
    c = json.loads(resp.text)['data']
    print(c)
    return {'buvid3': c['b_3'], 'buvid4': c['b_4']}


def getstart(roomid=30195379, buvid=None):
    callback.set_roomid(roomid)
    if buvid is None:
        buvid = getcookie()
    print('获取弹幕流')
    cookie = loginfo.update(buvid)
    resp = requests.get(f"https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo?id={roomid}",
                        headers=header, cookies=loginfo)
    data = json.loads(resp.text)['data']
    key = data['token']
    host = data['host_list'][0]['host']
    port = data['host_list'][0]['ws_port']
    print(data)
    return {'key': key, 'uri': f'ws://{host}:{port}/sub', 'roomid': roomid, 'buvid': buvid}


async def getaudience(roomid=30195379):
    while True:
        resp = requests.get(f'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={roomid}', headers=header)
        resp = json.loads(resp.text)
        callback.audience(resp['data']['online'])
        await asyncio.sleep(10)


async def auth(websocket, sinfo):
    req = proto.Proto()
    req.body = json.dumps(
        {"uid": Myuid, "roomid": sinfo['roomid'], "protover": 3, "platform": "web", "type": 2, "key": sinfo['key'],
         "buvid": sinfo['buvid']['buvid3']})
    req.op = 7
    req.ver = 1
    await websocket.send(req.pack())
    print("[BiliClient] send auth success")
    try:
        buf = await websocket.recv()
    except:
        print("auth 失败")
        quit()
    resp = proto.Proto()
    resp.unpack(buf)
    respBody = json.loads(resp.body)
    if respBody["code"] != 0:
        print("auth 失败")
    else:
        print("auth 成功")


async def heartBeat(websocket):
    while True:
        req = proto.Proto()
        req.op = 2
        req.ver = 1
        await websocket.send(req.pack())
        #print("[BiliClient] send heartBeat success")
        await asyncio.ensure_future(asyncio.sleep(20))


async def recvLoop(websocket):
    print("[BiliClient] run recv...")
    while True:
        recvBuf = await websocket.recv()
        resp = proto.Proto()
        # print("接收到", recvBuf)
        # try:
        #     print('zlib解密尝试:',zlib.decompress(recvBuf))
        # except:
        #     print('zlib解密失败,尝试brotli解密')
        #     try:
        #         print('brotli解密:',brotli.decompress(recvBuf))
        #     except:
        #         print('brotli解密失败，尝试gzip解密')
        #         try:
        #             print('gzip解密:',gzip.decompress(recvBuf))
        #         except:
        #             print('gzip解密失败,尝试UTF8解码')
        #             try:
        #                 print('UTF8解码:',recvBuf.decode('utf-8'))
        #             except:
        #                 print('UTF8解码失败,尝试GBK解码')
        resp.unpack(recvBuf)


async def connect(sinfo):
    ws = await websockets.connect(sinfo['uri'])
    await auth(ws, sinfo)
    return ws


def run(rid=30195379):
    info = getstart(roomid=rid)
    print(info)
    loop = asyncio.get_event_loop()
    # 建立连接
    websocket = loop.run_until_complete(connect(info))
    tasks = [
        # asyncio.ensure_future(getaudience(rid)),
        # 读取信息
        asyncio.ensure_future(recvLoop(websocket)),
        # 发送心跳
        asyncio.ensure_future(heartBeat(websocket)),
    ]
    loop.run_until_complete(asyncio.gather(*tasks))


# run() #rid=5399166
# getcookie()
if __name__ == '__main__':
    freeze_support()
    p = Process(target=run, args=(roomid,))
    while True:
        if login.is_living(roomid):
            if p.is_alive():
                time.sleep(15)
            else:
                callback.update_fn()
                p.start()
                print("start")
                time.sleep(15)
        else:
            if p.is_alive():
                p.terminate()
                time.sleep(15)
            else:
                time.sleep(15)
