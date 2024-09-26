import json
import time
import requests
import login

loginfo = login.login()
cookie = {'SESSDATA': loginfo['SESSDATA'],
          'bili_jct': loginfo['bili_jct'],
          }
csrf = loginfo['bili_jct']
ft = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
room_id = 0
filename = f'./logs/{ft}.log'
def update_fn():
    global filename
    filetime = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
    filename = f'./logs/{filetime}.log'
    print('Start Logging to:', filename)


def log(text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text + '\n')


def set_roomid(roomid):
    global room_id
    room_id = roomid
    log(f'room_id:{room_id}')


def getformattedtime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def audience(num):
    info = f"[AUDIE]{getformattedtime()}---当前观众数:{num}"
    print(info)
    log(info)


def callback(data):
    # print('callback:', data)
    try:
        data = json.loads(data)
    except:
        return
    # print(data)
    if data['cmd'] == "DANMU_MSG":
        info = f"[DANMU]{getformattedtime()}---{data['info'][2][1]}({data['info'][2][0]}):{data['info'][1]}"
        # with open('chat.log', 'a', encoding='utf-8') as f:
        #     f.write(info+'\n')
        print(info)
        log(info)
        # senddm(msg['content'])
    elif data['cmd'] == "STOP_LIVE_ROOM_LIST":
        pass
    elif data['cmd'] == "INTERACT_WORD":
        data = data['data']
        if data['msg_type'] == 1:
            info = f"[GETIN]{getformattedtime()}---{data['uname']}({data['uid']})进入直播间"
            print(info)
            log(info)
        #     senddm(f'欢迎{data["uname"]}大人进入直播间!')

        if data['msg_type'] == 2 or data['msg_type'] == 5:
            info = f"[NFANS]{getformattedtime()}---{data['uname']}({data['uid']})关注了直播间"
            print(info)
            # senddm(f'感谢{data["uname"]}大人的关注!')
            log(info)

    elif data['cmd'] == "ENTRY_EFFECT":
        pass
        # uname = ''
        # data = data['data']
        # rtext = data["copy_writing"]
        # sindex = rtext.find('<%')
        # eindex = rtext.find('%>')
        # if sindex != -1 and eindex != -1:
        #     uname = rtext[sindex+2:eindex]
        # senddm('欢迎'+uname+'大人进入直播间!')

    elif data['cmd'] == "SEND_GIFT":
        data = data['data']
        info = f'[GIFTS]{getformattedtime()}---{data["uname"]}({data["uid"]}){data["action"]}了{data["num"]}个{data["giftName"]}'
        print(info)
        log(info)
    elif data['cmd'] == "POPULARITY_RED_POCKET_NEW":
        data = data['data']
        info = f'[RPOCK]{getformattedtime()}---{data["uname"]}({data["uid"]})送出了红包({data["price"]}电池)'
        print(info)
        log(info)
    elif data['cmd'] == "POPULARITY_RED_POCKET_WINNER_LIST":
        print('红包中奖名单记录正在加急开发中')
    elif data['cmd'] == "GUARD_BUY":
        data = data['data']
        info = f'[GUARD]{getformattedtime()}---{data["username"]}({data["uid"]})开通了{data["gift_name"]}({data["num"]}个月)'
        print(info)
        log(info)
    elif data['cmd'] == "SUPER_CHAT_MESSAGE":
        data = data['data']
        info = f'[NEWSC]{getformattedtime()}---{data["user_info"]["uname"]}({data["uid"]})送出了{data["price"]}元SC:{data["message"]}'
        print(info)
        log(info)
    elif data['cmd'] == "LIKE_INFO_V3_UPDATE":
        data = data['data']
        info = f'[LIKES]{getformattedtime()}---当前直播间点赞数:{data["click_count"]}'
        print(info)
        log(info)
    elif data['cmd'] == "ROOM_CHANGE":
        data = data['data']
        info = f'[RCHGE]{getformattedtime()}---主播更改了直播间信息:标题->{data["title"]}分区->{data["area_name"]}'
        print(info)
        log(info)
    elif data['cmd'] == "DM_INTERACTION":
        pass
    #     data = json.loads(data['data']['data'])['suffix_text']
    #     info = f'[DANMU]{getformattedtime()}---观众们(000000000):{data}'
    #     print(info)
    #     log(info)
    elif data['cmd'] == "DANMU_AGGREGATION":
        data = data['data']
        info = f"[DANMU]{getformattedtime()}---观众们(000000000):{data['msg']}"
        print(info)
        log(info)

    elif data['cmd'] == "ONLINE_RANK_COUNT":
        data = data['data']
        info = f"[AUDIE]{getformattedtime()}---当前观众数:{data['online_count']}"
        print(info)
        log(info)
    elif data['cmd'] == "COMBO_SEND":
        data = data['data']
        info = f'[GIFTS]{getformattedtime()}---{data["sender_uinfo"]["base"]["name"]}({data["sender_uinfo"]["uid"]}){data["action"]}了{data["combo_num"]}个{data["gift_name"]}'
    else:
        print('敬请期待' + data['cmd'])
        print(data)
        pass


def senddm(word):
    print(room_id)
    url = 'https://api.live.bilibili.com/msg/send'
    data = {
        'bubble': '0',
        'msg': word,
        'color': '16777215',
        'mode': '1',
        'dm_type': '0',
        'room_type': '0',
        'jumpfrom': '86002',
        'reply_mid': '0',
        'reply_attr': '0',
        'replay_dmid': 'statistics:{"appId":100,"platform":5}',
        'fontsize': '25',
        'rnd': '1724486302',
        'roomid': str(room_id),
        'csrf': csrf,
        'csrf_token': csrf,
    }
    headers = {
        'origin': 'https://live.bilibili.com',
        'priority': 'u=1, i',
        'referer': f'https://live.bilibili.com/{room_id}?broadcast_type=0&is_room_feed=1&spm_id_from=333.999.to_liveroom.0.click&live_from=86002',
        'ec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }
    response = requests.post(url=url, data=data, headers=headers, cookies=cookie)
    if response.status_code == 200:
        print(f'发送成功,本次的发送内容是：{word}')
        print(response.text)
    else:
        print('发送失败')
