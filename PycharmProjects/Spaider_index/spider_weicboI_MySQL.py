# coding=utf-8
import urllib
import urllib.request
import re
import xlwt, time, xlrd
import socket
import pymysql
import datetime

# from datetimeshz import date_time

# 连接服务器
db = pymysql.connect("localhost", "root", "qwer1234", "skin_database", charset="utf8")
cursor = db.cursor()
sql = '''replace into weibo_index(关键字,日期,整体趋势,PC趋势,移动趋势)
values
(%s,%s,%s,%s,%s)'''


# 待搜索关键字
# searchList = ['中国电信股份有限公司上海分公司','上海市电信有限公司','上海电信']
def date_time(delta):
    now = datetime.date.today()
    delta2 = datetime.timedelta(days=1)
    delta = datetime.timedelta(days=delta)
    n_days = now - delta2 - delta
    return (n_days.strftime('%Y-%m-%d'))


# day = time.strftime("%Y-%m-%d", time.localtime())
# day_before = time.strftime("%Y-%m-%d", time.localtime(time.mktime(time.localtime())-86400))
# print(day_before)

with open('./keyword.txt') as f:
    searchList = f.readlines()

dictList = {'去屑': '1091324129498', '牙膏': '1091324255263', '卸妆': '1091324128746', '防晒': '1091324347251',
            '隔离': '1091324353714',
            '染发': '1091324222836', '保湿': '1091324103589', '抗衰老': '1091323827155', '唇膏': '1091324139558',
            '美白': '1091324293088',
            '洁面': '1091324243096', '化妆水': '1091323944194', '面膜': '1091324358170', '粉底液': '1091323824303',
            '睫毛膏': '1091323823850',
            '唇笔': '1091324139552', 'BB霜': '1060000053069', '彩妆盘': '1091323831386', '定妆': '1091324164908',
            '粉饼': '1091324281622',
            '眼影': '1091324269642', '遮瑕': '1091324337304', '高光': '1091324448368', '粉底': '1091324281525',
            '蜜粉': '1091324316011',
            '眼线': '1091324269696', '腮红': '1091324298942', '假睫毛': '1091323824534', '指甲油': '1091323823938',
            '眉笔': '1091324269319',
            '唇彩': '1091324139539', '香水': '1091324361598', '假发': '1091324104926', '欧莱雅男士': '1011886467911',
            '妮维雅男士': '1011307102642102105',
            '杰威尔': '1091324220507', '锐度': '1091324344898', '高夫': '1091324365971', '曼秀雷敦': '1030000003583',
            '植美村': '1091324229256', '玛丽黛佳': '1091324258748',
            '卡姿兰': '1091324125427', '欧诗漫': '1091324472037', '巧迪尚惠': '1091324173068', '韩后': '1011985391034',
            '美肤宝': '1091324293154', '美丽加芬': '1091324292592',
            '力士': '1030000003301', '拉芳': '1091324200046', '舒肤佳': '1091324300176', '强生婴儿': '1012505935841',
            '所望': '1091324194998', '菲诗小铺': '1030000001746'}


# title = [u'日期',u'综合',u'pc',u'mobile']
# 以上lists
def spider_weibo_index():
    f = open(r'./proxy')
    lines = f.readlines()
    proxys = []
    datelist = []
    keywordlist = []
    totallist = []
    pclist = []
    mobilelist = []

    for i in range(0, len(lines)):
        ip = lines[i].strip("\n").split("\t")
        proxy_host = "http://" + ip[0] + ":" + ip[1]
        proxy_temp = {"http": proxy_host}
        proxys.append(proxy_temp)
    # 以上ip代理

    for i in range(len(searchList)):
        param = []
        id = dictList[searchList[i].strip()]
        data = {}
        url_values = urllib.parse.urlencode(data)
        # url = "http://data.weibo.com/index/ajax/getchartdata?wid=" + id + "&sdate=" + date_time(
        #     0) + "&edate=" + date_time(0) + "&__rnd=1489742022522"
        url = "http://data.weibo.com/index/ajax/getchartdata?wid=" + id + "&sdate=2016-1-1" +  "&edate=" + date_time(0) + "&__rnd=1489742022522"

        full_url = url + url_values
        user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
        referer = 'http://data.weibo.com/index/hotword?wid=' + id + '&wname=%E9%98%B2%E6%99%92'

        headers = {'User_Agent': user_agent,
                   'Referer': referer}
        time.sleep(1)
        for proxy in proxys:
            try:
                request = urllib.request.Request(full_url, headers=headers)
                data = urllib.request.urlopen(request, timeout=100000).read()
                data = data.decode('utf-8')
                # print(data)
                sitems = data.split('yd')
                pattern1 = re.compile('.*?day_key":"(.*?)","wid":"(.*?)","value":"(.*?)"},', re.S)
                items1 = re.findall(pattern1, sitems[0])
                pattern2 = re.compile('.*?daykey":"(.*?)","pc":"(.*?)","mobile":"(.*?)"}', re.S)
                items2 = re.findall(pattern2, sitems[1])
                for s in range(len(items1)):
                    param.append((searchList[i].strip(), items1[s][0], items1[s][2], items2[s][1], items2[s][2]))
                print(param)
                # for i in range(len(param)):
                #     cursor.executemany(sql.format(value=param[i]))
                #     db.commit()
                cursor.executemany(sql,param)
                db.commit()
                time.sleep(3)
                # keywordlist.append(searchList[i])
                # datelist.append(items1[s][0])
                # totallist.append(items1[s][2])
                # pclist.append(items2[s][1])
                # mobilelist.append(items2[s][2])
                #  dfdata = {"keyword": keywordlist,
                #  "date_time": datelist,
                #  "total": totallist,
                #  "pc": pclist,
                #  "mobile": mobilelist,
                # }
                # df = pd.DataFrame(data=dfdata)
                # lenn = len(df)
                # if lenn > 0:
                #     df.to_sql("weiboindex", conn, if_exists='append', index=False)
                # for s in range(len(items1)):
                #     cursor.execute ("insert into weiboindex(keyword,date_time,total,pc,mobile) values(searchList[i],items1[s][0],items1[s][2],items2[s][1],items2[s][2])")  
                # # # for s in range(len(items1)):
                #     ws.write(1+s,0,items1[s][0])
                #     ws.write(1+s,1,items1[s][2])
                #     ws.write(1+s,2,items2[s][1])
                #     ws.write(1+s,3,items2[s][2])
                print('success')
                break
            except Exception as e:
                print(proxy)
                print(e)
                continue

    cursor.close()
    db.close()


def wb2mysql():
    spider_weibo_index()
    time.sleep(86400)
    return wb2mysql()


if __name__ == '__main__':
    wb2mysql()
