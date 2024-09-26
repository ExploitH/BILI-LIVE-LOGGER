import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
fl = os.listdir('../logs')
#找到最新的log
fl.sort()
fn = fl[-1]
# fn = '20240925_2009.log'
print('目前绘图所使用的日志：', fn)
# fn = '20240924_1618.log'
dire = f"./{fn[4:6]}-{fn[6:14].replace('_','-')}/"

def tra(txt: str):
    if txt == 'DANMU':
        return '分钟内弹幕数'
    elif txt == 'GIFTS':
        return '分钟内礼物数'
    elif txt == 'GETIN':
        return '分钟内进房数'
    elif txt == 'GUARD':
        return '分钟内上舰数'
    elif txt == 'LIKES':
        return '点赞总数'
    elif txt == 'NFANS':
        return '分钟内新关注数'

def exp(info: str):
    mtype = info[1:6]
    mtime = info[7:26]
    # print(mtime, mtype)
    # ptime = time.strptime(mtime, '%Y-%m-%d %H:%M:%S')
    return mtime, mtype
    # print(ptime, mtype)
lst = []
with open(f'../logs/{fn}', 'r', encoding='utf-8') as f:
    for line in f:
        if 'room_id:' in line:
            continue
        lst.append(exp(line))
def draw(mtype: str, num=1):
    tlist = []
    tclist = []
    prv = ''
    cnt = 0
    for i in lst:
        if i[0][5:16] == prv:
            if i[1] == mtype:
                cnt += 1
        else:
            tclist.append(cnt)
            cnt = 0
            prv = i[0][5:16]
            tlist.append(prv)
    tclist.append(cnt)
    tclist.pop(0)
    if len(tlist) != len(tclist):
        print('error')
    plt.figure(num=num, figsize=(32, 18))
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.rcParams['font.family'] = ['Microsoft YaHei']
    plt.rcParams['font.size'] = 14
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.autoscale(enable=True, axis='y', tight=False)
    plt.xlabel('时间')
    plt.ylabel('计数')
    plt.title(tra(mtype))
    plt.plot(tlist, tclist)
    plt.xticks(rotation=90)
    try:
        plt.savefig(dire + mtype + '.png')
    except:
        os.mkdir(dire)
        plt.savefig(dire + mtype + '.png')
    # plt.show()
    # plt.legend(['count'])

def drawlikes(num=1):
    tl = []
    ll = []
    with open(f'../logs/{fn}', 'r', encoding='utf-8') as fi:
        for l in fi:
            if 'room_id:' in l:
                continue
            elif '[LIKES]' in l:
                tl.append(l[18:26])
                ll.append(int(l.split(':')[-1]))
    plt.figure(num=num, figsize=(32, 18))
    plt.rcParams['font.family'] = ['Microsoft YaHei']
    plt.rcParams['font.size'] = 14
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.autoscale(enable=True, axis='y', tight=False)
    plt.xlabel('时间')
    plt.ylabel('计数')
    plt.title('点赞总数')
    plt.plot(tl, ll)
    plt.xticks(rotation=90)
    # print(tl)
    # print(ll)
    try:
        plt.savefig(dire+"LIKES.png")
    except:
        os.mkdir(dire)
        plt.savefig(dire+"LIKES.png")

def drawaudience(num=1):
    tl = []
    ll = []
    with open(f'../logs/{fn}', 'r', encoding='utf-8') as fi:
        for l in fi:
            if 'room_id:' in l:
                continue
            elif '[AUDIE]' in l:
                tl.append(l[18:26])
                ll.append(int(l.split(':')[-1]))
    plt.figure(num=num, figsize=(32, 18))
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.rcParams['font.family'] = ['Microsoft YaHei']
    plt.rcParams['font.size'] = 14
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.autoscale(enable=True, axis='y', tight=False)
    plt.xlabel('时间')
    plt.ylabel('计数')
    plt.title('观众总数')
    plt.plot(tl, ll)
    plt.xticks(rotation=90)
    try:
        plt.savefig(dire+"AUDIE.png")
    except:
        os.mkdir(dire)
        plt.savefig(dire+"AUDIE.png")

def drawall():
    draw('DANMU', num=1)
    draw('GETIN', num=2)
    draw('GIFTS', num=3)
    draw('NFANS', num=4)
    draw('GIFTS', num=5)
    # draw('RPORK')
    draw('GUARD', num=6)
    drawlikes(num=7)
    drawaudience(num=8)
    print('绘图完成,保存至"Graphic"文件夹下的', dire, '中')

drawall()