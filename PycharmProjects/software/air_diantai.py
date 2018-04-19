# -*- coding:utf-8 -*-
import urllib, urllib.request
import re
import xlwt, time, xlrd
from bs4 import BeautifulSoup
import sys
import simplejson
import datetime
from threading import Timer

# import cx_Oracle  ,


title = ['设备编号', '创建时间', '查询时间', '温度', '湿度', 'pm25', 'pm10']
# searchList = ['7300049BB8EE','7300068888AA','73000332EC53','7300087414A7','730002868287','730007D84CC3','730001B84C05','7300057E0270','7300060008BA','730004CA6CA4','730009471592','730002139E54','730002341B00','730002F291B9','73000437DE9A','73000825C0ED','73000414DF8E','730005489726','73000240083E','730006E10757','730003160A37','730006AD4FDE','7300083054AF','730005CA5D97','73000451BE96','730005D6E044','73000651DCF0','73000404EE9C','73000493B06F','730005C01736','73000375CF6B','7300060129AA','7300090117BA','7300061039A8','73000514EEBD','73000269438B','730005D10734','730004739E92','730005D26404','730004D01717']
searchList = ['7300049BB8EE', '7300068888AA', '73000332EC53', '7300087414A7', '730002868287',
              '730007D84CC3', '730001B84C05', '7300057E0270', '7300060008BA', '730004CA6CA4', '730009471592',
              '730002139E54', '730002341B00', '730002F291B9', '73000437DE9A', '73000825C0ED', '73000414DF8E',
              '730005489726', '73000240083E', '730006E10757', '730003160A37', '730002F734E9', '7300083054AF',
              '730005CA5D97', '73000451BE96', '730005D6E044', '73000651DCF0', '73000404EE9C', '73000493B06F',
              '730005C01736', '73000375CF6B', '730007665985', '7300090117BA', '7300061039A8', '73000514EEBD',
              '73000269438B', '730005D10734', '730004739E92', '730003C9980D', '730004D01717',  # 以上是强生项目
              '73000395E196', '730005324AF9', '73000949DB73', '7300092216AE', '730005178D8D', '73000662913D',
              # 以下是体重项目的设备
              '73000959EA61', '730001C1F2EA', '730002705B08', '730003BA6C43', '730006278DEE', '730006191039',
              '7300095447B0', '73000862E3D5', '73000459B617', '730005B08048', '730001CBB84B', '7300050FB41F',
              '730001B4C0C4', '73000693D209', '73000625CFCE', '730010F9EB6D'
              # '7300170DE75B','7300166E1334','730016C91EF1','7300167F0336' #2017-6-5 厂家更换设备
              ]

f = open(r'G:\舒慧珍\空气电台\src\proxy')
lines = f.readlines()
proxys = []
rank = 0
w = xlwt.Workbook()
ws = w.add_sheet('空气指数', cell_overwrite_ok=True)

for i in range(0, len(lines)):
    ip = lines[i].strip("\n").split("\t")
    proxy_host = "http://" + ip[0] + ":" + ip[1]
    proxy_temp = {"http": proxy_host}
    proxys.append(proxy_temp)
# 以上ip代理

timer_interval = 1


def delayrun():
    print('running')


t = Timer(timer_interval, delayrun)
t.start()
while True:
    time.sleep(30)
    try:
        for i in range(len(searchList)):
            rank += 1
            id = searchList[i]

            url = 'http://weiguo.airradio.cn/smart/hwmobile/smart/cloudOuter!getCorpDevices?SENSORIDS=' + id + '&KEY=frevdl3g'
            print(url)
            time.sleep(2)
            user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
            headers = {'User_Agent': user_agent}
            for proxy in proxys:
                try:
                    # url=urllib.parse.quote(url)
                    request = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(request)
                    content = response.read()
                    soup = BeautifulSoup(content, "html.parser")

                    dict1 = simplejson.loads(soup.prettify())
                    dict2 = simplejson.loads(dict1['dataObject'])
                    print(dict2[id]['param']['SensorNo_2_SensorData'])

                    temperature = dict2[id]['param']['SensorNo_2_SensorData']
                    humidity = dict2[id]['param']['SensorNo_3_SensorData']
                    pm2_5 = dict2[id]['param']['SensorNo_4_SensorData']
                    pm10 = dict2[id]['param']['SensorNo_5_SensorData']
                    createtime = dict2[id]['createTime']
                    querytime = dict2[id]['queryTime']

                    for i in range(len(title)):
                        ws.write(0, i, title[i])
                        ws.write(rank, 0, id)
                        ws.write(rank, 1, createtime)
                        ws.write(rank, 2, querytime)
                        ws.write(rank, 3, temperature)
                        ws.write(rank, 4, humidity)
                        ws.write(rank, 5, pm2_5)
                        ws.write(rank, 6, pm10)

                    # param.append((searchList[i],querytime(s),index_tb[len(index_1688)-1-s],indexcts_tb[len(index_1688)-1-s],index_1688[len(index_1688)-1-s],indexcts_1688[len(index_1688)-1-s],index_supply[len(index_1688)-1-s],indexcts_supply[len(index_1688)-1-s]))
                    # print(param)

                    # cursor.executemany('insert into temp_shz_aliindex_0411 values(:1,:1,:1,:1,:1,:1,:1,:1)',param);
                    # cursor.execute('insert into TEMP_SHZ_AIR_0426 values(ddd,ddd,ddd,ddd,ddd,ddd)');
                    # cursor.execute('insert into TEMP_SHZ_AIR_0426 values(id,querytime,temperature,humidity,pm2_5,pm10)');
                    # cursor.execute('insert into CESHI_AIR_0426 select * from TEMP_SHZ_AIR_0426 where device_id||date_time not in (select kdevice_id||date_time from CESHI_AIR_0426)');
                    # cursor.execute('truncate table TEMP_SHZ_AIR_0426')

                    print('success')
                    break
                except urllib.request.URLError as e:
                    if hasattr(e, "code"):
                        print(e.code)
                    if hasattr(e, "reason"):
                        print(e.reason)
            w.save(r'G:\舒慧珍\空气电台\air.xls')

    except:
        continue
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

# coding: utf-8

# In[1]:


# -*- coding:utf-8 -*-
import cx_Oracle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdate
from pylab import *
import xlwt

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体

mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 定义设备编号和使用者所属人群

device_ids = ['7300049BB8EE', '7300087414A7', '7300057E0270', '730002F291B9', '73000825C0ED', '73000240083E',
              '730006AD4FDE', '730005D6E044', '730005C01736', '730003C9980D', '730002F734E9', '730008888789',
              '730006B2913D',  # 家庭主妇
              '730007D84CC3', '730002139E54', '73000437DE9A', '73000414DF8E', '730005489726', '73000651DCF0',
              '7300095447B0',
              '73000493B06F', '73000375CF6B', '73000269438B', '73000693D209', '730016C91EF1', '730010F9EB6D',  # 室内工作者
              '7300068888AA', '7300060008BA', '730009471592', '730002341B00', '730006E10757', '730003160A37',
              '7300083054AF',
              '730005CA5D97', '7300060129AA', '73000514EEBD', '73000459B617', '7300170DE75B', '730007665985',  # 室外工作者
              '73000332EC53', '730002868287', '730004CA6CA4', '73000451BE96', '73000404EE9C', '7300090117BA',
              '7300061039A8',
              '730005D10734', '730004739E92', '730004D01717', '73000959EA61', '7300050FB41E', '73000862E3D5',
              '7300092216AE']
sdevice = ['730010F9EB6D', '730016C91EF1', '7300170DE75B', '7300166E1334', '7300167F0336']

decive_ids_dict = {'7300049BB8EE': 'no1', '7300087414A7': 'no2', '7300057E0270': 'no3', '730002F291B9': 'no4',
                   '730008888789': 'no4', '73000825C0ED': 'no5',
                   '73000240083E': 'no6', '730006AD4FDE': 'no7', '730005D6E044': 'no8', '730005C01736': 'no9',
                   '730003C9980D': 'no10', '730006B2913D': 'no10',
                   '730002F734E9': 'no7', '730007D84CC3': 'no11', '7300095447B0': 'no11', '730002139E54': 'no12',
                   '73000437DE9A': 'no13', '73000414DF8E': 'no14',
                   '730005489726': 'no15', '73000651DCF0': 'no16', '73000493B06F': 'no17', '73000375CF6B': 'no18',
                   '73000269438B': 'no19',
                   '73000693D209': 'no17', '730010F9EB6D': 'no17', '730016C91EF1': 'no18', '7300068888AA': 'no20',
                   '7300060008BA': 'no21', '73000459B617': 'no21',
                   '730009471592': 'no22', '730002341B00': 'no23', '7300170DE75B': 'no23', '730006E10757': 'no24',
                   '730003160A37': 'no25', '7300083054AF': 'no26',
                   '730005CA5D97': 'no27', '7300060129AA': 'no28', '730007665985': 'no28', '73000514EEBD': 'no29',
                   '730007665985': 'no28', '73000332EC53': 'no30',
                   '730002868287': 'no31', '73000959EA61': 'no31', '730004CA6CA4': 'no32', '73000451BE96': 'no33',
                   '73000404EE9C': 'no34', '7300050FB41E': 'no34', '7300090117BA': 'no35', '7300092216AE': 'no35',
                   '7300061039A8': 'no36', '73000862E3D5': 'no36', '730005D10734': 'no37', '730004739E92': 'no38',
                   '730004D01717': 'no39'}
housewife = ['7300049BB8EE', '7300087414A7', '7300057E0270', '730002F291B9', '73000825C0ED', '73000240083E',
             '730006AD4FDE', '730005D6E044', '730005C01736', '730003C9980D', '730002F734E9', '730008888789',
             '730006B2913D']
indoor = ['730007D84CC3', '7300095447B0', '730002139E54', '73000437DE9A', '73000414DF8E', '730005489726',
          '73000651DCF0', '73000493B06F', '73000375CF6B', '73000269438B', '73000693D209', '730016C91EF1',
          '730010F9EB6D']
outdoor = ['7300068888AA', '7300060008BA', '730009471592', '730002341B00', '730006E10757', '730003160A37',
           '7300083054AF', '730005CA5D97', '7300060129AA', '73000514EEBD', '73000459B617', '7300170DE75B',
           '730007665985']
student = ['73000332EC53', '730002868287', '730004CA6CA4', '73000451BE96', '73000404EE9C', '7300090117BA',
           '7300061039A8', '730005D10734', '730004739E92', '730004D01717', '73000959EA61', '7300050FB41E',
           '73000862E3D5', '7300092216AE']
category = [housewife, indoor, outdoor, student]
renqun = ['家庭主妇', '室内工作者', '室外工作者', '学生']
# 定义每个人开始测试的时间
startdict = {'no1': '526', 'no2': '525', 'no3': '527', 'no4': '525', 'no5': '526', 'no6': '523', 'no7': '526',
             'no8': '523', 'no9': '525', 'no10': '527', 'no11': '525',
             'no12': '524', 'no13': '523', 'no14': '524', 'no15': '523', 'no16': '525', 'no17': '524', 'no18': '526',
             'no19': '523', 'no20': '524', 'no21': '523', 'no22': '527',
             'no23': '524', 'no24': '527', 'no25': '523', 'no26': '526', 'no27': '526', 'no28': '524', 'no29': '523',
             'no30': '525', 'no31': '526', 'no32': '525', 'no33': '523',
             'no34': '524', 'no35': '526', 'no36': '524', 'no37': '526', 'no38': '524', 'no39': '524'}

import math

conn = cx_Oracle.connect('account/psssword@192.168.1.18/database')
cursor = conn.cursor()
# 从数据库读取数据
cursor.execute(
    "SELECT DEVICE_ID ,query_time,newcteate_time,humidity,temperature,PM2_5,PM10,to_char(newcteate_time,'yyyy-mm-dd hh24:mi:ss') FROM ceshi_airsensor where newcteate_time>to_date('2017-05-23 00:00:00','yyyy-mm-dd hh24:mi:ss')and newcteate_time<to_date('2017-07-26 09:00:00','yyyy-mm-dd hh24:mi:ss')order by device_id,newcteate_time")
print('数据读入')

row = cursor.fetchall()


# 在读取数据的同时添加数据的变量等级标签，不同的时间标签
def getresult(id):
    for i in range(len(row)):

        if row[i][0] == id:
            id_num = decive_ids_dict[id]
            weektype = row[i][2].isocalendar()[1]  # 在日历上第几周
            delta = datetime.datetime(2017, 5, 18, 12, 19, 17) - datetime.datetime(2017, 5, 18, 12, 19, 17)
            PM25type = 0
            if row[i - 1][0] == id:
                delta = row[i][2] - row[i - 1][2]
            else:
                delta = datetime.datetime(2017, 5, 18, 12, 19, 17) - datetime.datetime(2017, 5, 18, 12, 19, 17)
            delta = delta.seconds / 3600
            tempertype = None
            wurantype = None
            PM25type = None
            humitype = None
            if int(row[i][5]) < 100:
                PM25type = '0良好'
                wurantype = '0'
            elif int(row[i][5]) >= 100 and int(row[i][5]) < 150:
                PM25type = '1轻度污染'
            elif int(row[i][5]) >= 150 and int(row[i][5]) < 200:
                PM25type = '2中度污染'
            elif int(row[i][5]) >= 200 and int(row[i][5]) < 300:
                PM25type = '3重度污染'
            elif int(row[i][5]) >= 300 and int(row[i][5]) < 500:
                PM25type = '4严重污染'
            elif int(row[i][5]) >= 500:
                PM25type = '5超严重污染'

            if int(row[i][5]) < 100:
                wurantype = '0'
            elif int(row[i][5]) >= 100:
                wurantype = '1'
            if int(row[i][3]) < 40:
                humitype = '偏干'
            elif int(row[i][3]) >= 40 and int(row[i][3]) < 60:
                humitype = '中等'
            elif int(row[i][3]) >= 60:
                humitype = '偏湿'

            if int(row[i][4]) >= 5 and int(row[i][4]) < 14:
                tempertype = '凉'
            elif int(row[i][4]) >= 14 and int(row[i][4]) < 18:
                tempertype = '暖1'
            elif int(row[i][4]) >= 18 and int(row[i][4]) < 22:
                tempertype = '暖2'
            elif int(row[i][4]) >= 22 and int(row[i][4]) < 24:
                tempertype = '热1'
            elif int(row[i][4]) >= 24 and int(row[i][4]) < 26:
                tempertype = '热2'
            elif int(row[i][4]) >= 26 and int(row[i][4]) < 28:
                tempertype = '热3'
            elif int(row[i][4]) >= 28 and int(row[i][4]) < 30:
                tempertype = '热4'
            elif int(row[i][4]) >= 30 and int(row[i][4]) < 32:
                tempertype = '热5'
            elif int(row[i][4]) >= 32 and int(row[i][4]) < 34:
                tempertype = '热6'
            elif int(row[i][4]) >= 34 and int(row[i][4]) < 36:
                tempertype = '热7'
            elif int(row[i][4]) >= 36:
                tempertype = '热8'

            if row[i][0] in housewife:
                idtype = renqun[0]
            elif row[i][0] in indoor:
                idtype = renqun[1]
            elif row[i][0] in outdoor:
                idtype = renqun[2]
            elif row[i][0] in student:
                idtype = renqun[3]
            timetag = str(row[i][7][11:13]) + str(row[i][7][14])  # 获取时间：235，代表23点50分
            timetag1 = str(row[i][7][11:13]) + str(row[i][7][14])  # 获取时间：23，代表23点
            daytag = str(row[i][7][6]) + str(row[i][7][8:10])
            testtime = 'null'
            if daytag == startdict[id_num] and int(timetag1) < 17 and int(timetag1) > 9:  # 获取bl之后8小时,打上标签
                testtime = 'h8'

            hour8 = datetime.datetime.strptime(startdict[id_num], "%m%d")  # 获取8小时测试当日日期
            week1 = datetime.datetime.strptime(startdict[id_num], "%m%d") + datetime.timedelta(days=7)  # 获取一周测试当日日期
            week4 = datetime.datetime.strptime(startdict[id_num], "%m%d") + datetime.timedelta(days=28)  # 获取四周测试当日日期
            week8 = datetime.datetime.strptime(startdict[id_num], "%m%d") + datetime.timedelta(days=56)  # 获取八周测试当日日期
            aa = datetime.datetime.strptime(daytag, "%m%d")
            bb = datetime.datetime.strptime(startdict[id_num], "%m%d")
            weeklast = math.floor(((aa - bb).days) / 7) + 1  # 获得个体开始几周信息
            testday = 'null'
            threeday = 'null'
            if aa == week1:
                testday = 'test_w1'
            elif aa == week4:
                testday = 'test_w4'
            elif aa == week8:
                testday = 'test_w8'
            elif aa == hour8:
                testday = 'test_hour8'
            testday_3d = 'null'
            if aa > week1 - datetime.timedelta(days=2) and aa <= week1:
                testday_3d = 'test_w1_3d'
            if aa > week4 - datetime.timedelta(days=2) and aa <= week4:
                testday_3d = 'test_w4_3d'
            if aa > week8 - datetime.timedelta(days=2) and aa <= week8:
                testday_3d = 'test_w8_3d'
            if aa >= hour8 - datetime.timedelta(days=3) and aa < hour8:
                testday_3d = 'test_hour8_3d'
                threeday = -3
            if aa <= week8 + datetime.timedelta(days=3) and aa > week8:
                testday_3d = 'test_hour8_3d'
                threeday = 3
            if aa == hour8:
                threeday = 0
            # print(row[i][7])
            # 			print(aa)
            # 			print(bb)
            # 			print(weeklast)
            threedays.append(threeday)
            testday_3ds.append(testday_3d)
            testtimes.append(testtime)
            testdays.append(testday)
            weeklasts.append(weeklast)
            daytags.append(daytag)
            timetags.append(timetag)
            deltatimes.append(delta)
            ids.append(row[i][0])
            createtimes.append(row[i][2])
            humiditys.append(int(row[i][3]))
            temperatures.append(int(row[i][4]))
            PM2_5s.append(int(row[i][5]))
            PM10s.append(int(row[i][6]))
            PM25types.append(PM25type)
            idtypes.append(idtype)
            humitypes.append(humitype)
            tempertypes.append(tempertype)
            wurantypes.append(wurantype)
            id_nums.append(id_num)
            weektypes.append(weektype)
    print('执行至' + id)


cursor.close();
conn.commit();
conn.close();
threedays = []
testday_3ds = []
testtimes = []
testdays = []
ids = []
id_nums = []
createtimes = []
humiditys = []
temperatures = []
PM2_5s = []
PM10s = []
PM25types = []
idtypes = []
deltatimes = []
timetags = []
daytags = []
humitypes = []
tempertypes = []
wurantypes = []
weektypes = []
weeklasts = []
for i in range(len(device_ids)):
    getresult(device_ids[i])
for j in range(len(deltatimes)):
    if deltatimes[j] > 0.5:
        # print(deltatimes[i])
        deltatimes[j] = 0.02
for i in range(1, len(deltatimes)):
    deltatimes[i - 1] = deltatimes[i]
deltatimes[len(deltatimes) - 1] = 0


# In[39]:

# 获取数据异常值，计算异常值数量

def get_outlier(id):
    number = 0
    pianda25 = 0
    pianxiao25 = 0
    piandatep = 0
    ling25 = 0
    for i in range(len(ids)):
        if ids[i] == id:
            number += 1
            if PM2_5s[i]:
                if PM2_5s[i] > 900:
                    pianda25 += 1
                elif PM2_5s[i] < 10:
                    pianxiao25 += 1
                if PM2_5s[i] == 10:
                    ling25 += 1
            if temperatures[i]:
                if temperatures[i] > 40:
                    piandatep += 1
    if number != 0:
        return id, number, pianda25, pianda25 / number, pianxiao25, pianxiao25 / number, ling25, ling25 / number, piandatep, piandatep / number
    else:
        return id, number, pianda25, '没数据', pianxiao25, '没数据', ling25, '没数据', piandatep, '没数据'


titlelist = ['设备号', '总数据量', 'pm2.5偏大数据量', 'pm2.5偏大数量占比', 'pm2.5偏小数据量', 'pm2.5偏小数量占比', 'pm2.5为零数据量',
             'pm2.5为零数量占比', '温度偏大数据量', '温度偏大数量占比']
w = xlwt.Workbook()
ws = w.add_sheet('偏差数据量', cell_overwrite_ok=True)
for i in range(len(device_ids)):
    print(get_outlier(device_ids[i]))
    for q in range(10):
        ws.write(0, q, titlelist[q])
        ws.write(i + 1, q, get_outlier(device_ids[i])[q])

w.save(r'.\总体偏差数据量.xls')

# 将取出来的数据转成dataframe格式
for i in range(len(temperatures)):
    if temperatures[i] < 10:
        temperatures[i] = None
        # for i in range(len(humiditys)):
        #     if humiditys[i]>100:
        #         humiditys[i] = None
        # humiditys[i]>100 or
for i in range(len(ids)):
    if ids[i] in sdevice or humiditys[i] == 0:
        # print('错误湿度')
        humiditys[i] = None

data = {'ids': ids, 'createtimes': createtimes, 'humiditys': humiditys, 'temperatures': temperatures,
        'PM2_5s': PM2_5s, 'PM10s': PM10s, 'PM25types': PM25types, 'idtypes': idtypes, 'deltatimes': deltatimes,
        'daytags': daytags, 'timetags': timetags, 'humitypes': humitypes, 'tempertypes': tempertypes,
        'wurantypes': wurantypes, 'id_nums': id_nums, 'weektypes': weektypes, 'weeklasts': weeklasts,
        'testdays': testdays, 'testtimes': testtimes,
        'testday_3ds': testday_3ds, 'threedays': threedays}
frame = pd.DataFrame(data)
print('done')

groupedlast25 = frame['PM2_5s'].groupby([frame['id_nums'], frame['daytags'], frame['timetags']])
groupedid25 = frame['PM2_5s'].groupby([frame['id_nums'], frame['timetags']]).mean()

groupedlasttep = frame['temperatures'].groupby([frame['id_nums'], frame['daytags'], frame['timetags']])
groupedidtep = frame['temperatures'].groupby([frame['id_nums'], frame['timetags']]).mean()

groupedlasthum = frame['humiditys'].groupby([frame['id_nums'], frame['daytags'], frame['timetags']])
groupedidhum = frame['humiditys'].groupby([frame['id_nums'], frame['timetags']]).mean()
qunzudata = []

datalist = list(set(daytags))
datalist.sort()

timelist = ['000', '001', '002', '003', '004', '005', '010', '011', '012', '013', '014', '015',
            '020', '021', '022', '023', '024', '025', '030', '031', '032', '033', '034', '035', '040', '041',
            '042', '043', '044', '045', '050', '051', '052', '053', '054', '055', '060', '061', '062', '063',
            '064', '065', '070', '071', '072', '073', '074', '075', '080', '081', '082', '083', '084', '085',
            '090', '091', '092', '093', '094', '095', '100', '101', '102', '103', '104', '105', '110', '111',
            '112', '113', '114', '115', '120', '121', '122', '123', '124', '125', '130', '131', '132', '133',
            '134', '135', '140', '141', '142', '143', '144', '145', '150', '151', '152', '153', '154', '155',
            '160', '161', '162', '163', '164', '165', '170', '171', '172', '173', '174', '175', '180', '181',
            '182', '183', '184', '185', '190', '191', '192', '193', '194', '195', '200', '201', '202', '203',
            '204', '205', '210', '211', '212', '213', '214', '215', '220', '221', '222', '223', '224', '225',
            '230', '231', '232', '233', '234', '235']

print('done')

# 画出每个设备每天在24小时中的pm2.5变化情况

nolist = ['no1', 'no2', 'no3', 'no4', 'no5', 'no6', 'no7', 'no8', 'no9', 'no10', 'no11', 'no12', 'no13', 'no14', 'no15',
          'no16',
          'no17', 'no18', 'no19', 'no20', 'no21', 'no22', 'no23', 'no24', 'no25', 'no26', 'no27', 'no28', 'no29',
          'no30', 'no31', 'no32', 'no33', 'no34', 'no35', 'no36'
    , 'no37', 'no38', 'no39']
idsmade = []
datesmade = []
timesmade = []
for i in range(len(nolist)):
    for j in range(len(datalist)):
        for q in range(len(timelist)):
            idsmade.append(nolist[i])
            datesmade.append(datalist[j])
            timesmade.append(timelist[q])
dfmade = {'id_nums': idsmade, 'daytags': datesmade, 'timetags': timesmade}
dfmade['PM2_5s'] = np.zeros(len(nolist) * len(datalist) * len(timelist))
# print(len(idsmade),len(datesmade),len(timesmade),len(dfmade['PM2_5s'] ))
dfmade = pd.DataFrame(dfmade)
dfinalmade = dfmade.set_index(['id_nums', 'daytags', 'timetags'])
dfinal = groupedlast25.mean().reset_index().set_index(['id_nums', 'daytags', 'timetags'])
# print(dfinal)
# print(dfinalmade)
frame.set_index('id_nums')
dfadd = (dfinal + dfinalmade).fillna(27)
print(dfadd)
# 以上部分将空值补全
# 以下部分将粗曲线部分补全
idsmade1 = []
timesmade1 = []
for i in range(len(nolist)):
    for q in range(len(timelist)):
        idsmade1.append(nolist[i])
        timesmade1.append(timelist[q])
dfmade1 = {'id_nums': idsmade1, 'timetags': timesmade1}
dfmade1['PM2_5s'] = np.zeros(len(nolist) * len(timelist))
dfmade1 = pd.DataFrame(dfmade1)
dfinalmade1 = dfmade1.set_index(['id_nums', 'timetags'])
dfinal1 = groupedid25.reset_index().set_index(['id_nums', 'timetags'])
dfadd1 = (dfinal1 + dfinalmade1).fillna(27)
print(dfadd1)
# print(dfadd1.ix['7300049BB8EE'])
writer = pd.ExcelWriter('pm2.5day-change.xlsx')
dfadd1.reset_index().to_excel(writer, 'pm25')
writer.save()
# groupedid = groupedid.reset_index().set_index(['ids','timetags'])
for i in range(len(device_ids)):
    picid = device_ids[i]
    idtype = 'Null'
    if picid in housewife:
        idtype = '家庭主妇'
    elif picid in indoor:
        idtype = '室内'
    elif picid in outdoor:
        idtype = '室外'
    elif picid in student:
        idtype = '学生'
    picdays = []
    picdatas = []
    print(picid)
    picdatatotal = list(dfadd1.ix[decive_ids_dict[picid]].values[:, 0])
    # 	print(len(picdatatotal))
    for q in range(len(datalist)):
        picdays.append(datalist[q])
        picday = datalist[q]
        picdata = list(dfadd.ix[decive_ids_dict[picid]].ix[picday].values[:, 0])
        picdatas.append(picdata)
    # print(type(picdatas))

    hehe = []
    for i in range(144):
        hehe.append((i) / 6)
    X = np.array(hehe)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 7)
    plt.plot(X, picdatatotal, color='red', linewidth=2, linestyle="-", label='total')
    for p in range(len(datalist)):
        plt.plot(X, picdatas[p]  # ,color=colors[p]
                 , linewidth=1, linestyle="-", label=picdays[p])
    plt.xlabel('24小时', fontsize=20)
    plt.ylabel('pm2.5', fontsize=25)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(idtype + decive_ids_dict[picid], fontsize=25)
    # plt.legend(fontsize=12)
    plt.savefig('结果图片\不同设备pm2.5轨迹' + idtype + decive_ids_dict[picid] + '.png')
    plt.show()

print(len(frame))
pmmeanbyday = frame['PM2_5s'].groupby([frame['idtypes'], frame['id_nums'], frame['daytags']]).mean().reset_index()
hummeanbyday = frame['humiditys'].groupby([frame['idtypes'], frame['id_nums'], frame['daytags']]).mean().reset_index()
tepmeanbyday = frame['temperatures'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['daytags']]).mean().reset_index()
addallmean = pd.merge(frame, pmmeanbyday, on=['idtypes', 'id_nums', 'daytags'], how='left')
addallmean = pd.merge(frame, hummeanbyday, on=['idtypes', 'id_nums', 'daytags'], how='left')
addallmean = pd.merge(frame, pmmeanbyday, on=['idtypes', 'id_nums', 'daytags'], how='left')
print(len(addallmean))
# print(addallmean)


age_null = pd.isnull(addallmean['humiditys'])
age_null_true = age_null[age_null == True]
age_null_count = len(age_null_true)
print(age_null_count)

temperatures_null = pd.isnull(addallmean['temperatures'])
temperatures_null_true = temperatures_null[temperatures_null == True]
temperatures_null_count = len(temperatures_null_true)
print(temperatures_null_count)
# addallmean[addallmean.isnull().values==True]
addallmean.fillna({'humiditys': 'hummeanbyday', 'temperatures': 'tepmeanbyday'})

age_null1 = pd.isnull(addallmean['humiditys'])
age_null1_true = age_null[age_null1 == True]
age_null1_count = len(age_null1_true)
print(age_null1_count)

temperatures_null1 = pd.isnull(addallmean['temperatures'])
temperatures_null1_true = temperatures_null1[temperatures_null1 == True]
temperatures_null1_count = len(temperatures_null1_true)
print(temperatures_null1_count)

# In[22]:


pm8group = frame['PM2_5s'].groupby([frame['idtypes'], frame['id_nums'], frame['testtimes']]).mean().reset_index()
pmnowgroup = frame['PM2_5s'].groupby([frame['idtypes'], frame['id_nums'], frame['testdays']]).mean().reset_index()
pmnow_3group = frame['PM2_5s'].groupby([frame['idtypes'], frame['id_nums'], frame['testday_3ds']]).mean().reset_index()

hum8group = frame['humiditys'].groupby([frame['idtypes'], frame['id_nums'], frame['testtimes']]).mean().reset_index()
humnowgroup = frame['humiditys'].groupby([frame['idtypes'], frame['id_nums'], frame['testdays']]).mean().reset_index()
humnow_3group = frame['humiditys'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testday_3ds']]).mean().reset_index()

tep8group = frame['temperatures'].groupby([frame['idtypes'], frame['id_nums'], frame['testtimes']]).mean().reset_index()
tepnowgroup = frame['temperatures'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testdays']]).mean().reset_index()
tepnow_3group = frame['temperatures'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testday_3ds']]).mean().reset_index()

writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\pm2.5均值当天和8小时.xlsx')
pm8group.to_excel(writer, 'pm2.5均值8小时')
pmnowgroup.to_excel(writer, 'pm2.5均值当天')
pmnow_3group.to_excel(writer, 'pm2.5均值测试前三天')

hum8group.to_excel(writer, '湿度8小时')
humnowgroup.to_excel(writer, '湿度均值当天')
humnow_3group.to_excel(writer, '湿度均值测试前三天')

tep8group.to_excel(writer, '温度均值8小时')
tepnowgroup.to_excel(writer, '温度均值当天')
tepnow_3group.to_excel(writer, '温度均值测试前三天')

writer.save()

pmgroup = frame['PM2_5s'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['weeklasts'], frame['daytags'], frame['threedays']]).mean()
####删除设备no21
# del pmgroup['室外工作者','no21']
pmgroup = pmgroup.reset_index()
print(pmgroup)
writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\pm2.5均值按阶段.xlsx')
pmgroup.to_excel(writer, 'pm2.5均值')

writer.save()
pmgroupmean = pmgroup['PM2_5s'].groupby([pmgroup['idtypes']]).mean()
pmgroupstd = pmgroup['PM2_5s'].groupby([pmgroup['idtypes']]).std()
print(pmgroupmean)
print(pmgroupstd)

fig = plt.gcf()
fig.set_size_inches(22, 7)
x = np.arange(4)
plt.bar(x, pmgroupmean, width=0.2, label='pm2.5平均值')
plt.errorbar(x, pmgroupmean, yerr=pmgroupstd, fmt="o")
plt.xlabel('不同人群', fontsize=25)
plt.ylabel('pm2.5', fontsize=25)
for a, b in zip(x, pmgroupmean):
    plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=20)
# for a,b in zip(x,pmgroupstd):
#     plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'top',fontsize=17)
tags = ['学生', '室内工作者', '室外工作者', '家庭主妇']
plt.xticks(x, tags, rotation=0, fontsize=25)
plt.yticks(fontsize=20)
plt.title("空气电台", fontsize=25)
plt.legend()
plt.savefig('不同人群的pm2.5平均值.png')
plt.show()

# In[14]:


# 温度均值

tepgroup = frame['temperatures'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['weeklasts'], frame['daytags'], frame['threedays']]).mean()
####删除设备no21
# del pmgroup['室外工作者','no21']
tepgroup = tepgroup.reset_index()
print(tepgroup)
writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\温度均值阶段.xlsx')
tepgroup.to_excel(writer, '温度均值')

writer.save()
tepgroupmean = tepgroup['temperatures'].groupby([tepgroup['idtypes']]).mean()
tepgroupstd = tepgroup['temperatures'].groupby([tepgroup['idtypes']]).std()
print(tepgroupmean)
print(tepgroupstd)

fig = plt.gcf()
fig.set_size_inches(22, 7)
x = np.arange(4)
plt.bar(x, tepgroupmean, width=0.2, label='温度平均值')
plt.errorbar(x, tepgroupmean, yerr=tepgroupstd, fmt="o")
plt.xlabel('不同人群', fontsize=25)
plt.ylabel('温度', fontsize=25)
for a, b in zip(x, tepgroupmean):
    plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=20)
# for a,b in zip(x,pmgroupstd):
#     plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'top',fontsize=17)
tags = ['学生', '室内工作者', '室外工作者', '家庭主妇']
plt.xticks(x, tags, rotation=0, fontsize=25)
plt.yticks(fontsize=20)
plt.title("空气电台", fontsize=25)
plt.legend()
plt.savefig('不同人群的温度平均值.png')
plt.show()

# In[15]:


# 湿度均值

humgroup = frame['humiditys'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['weeklasts'], frame['daytags'], frame['threedays']]).mean()
####删除设备no21
# del pmgroup['室外工作者','no21']
humgroup = humgroup.reset_index()
print(humgroup)
writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\湿度均值阶段.xlsx')
humgroup.to_excel(writer, '湿度均值')

writer.save()
humgroupmean = humgroup['humiditys'].groupby([humgroup['idtypes']]).mean()
humgroupstd = humgroup['humiditys'].groupby([humgroup['idtypes']]).std()
print(humgroupmean)
print(humgroupstd)

fig = plt.gcf()
fig.set_size_inches(22, 7)
x = np.arange(4)
plt.bar(x, humgroupmean, width=0.2, label='湿度平均值')
plt.errorbar(x, humgroupmean, yerr=humgroupstd, fmt="o")
plt.xlabel('不同人群', fontsize=25)
plt.ylabel('湿度', fontsize=25)
for a, b in zip(x, humgroupmean):
    plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=20)
# for a,b in zip(x,pmgroupstd):
#     plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'top',fontsize=17)
tags = ['学生', '室内工作者', '室外工作者', '家庭主妇']
plt.xticks(x, tags, rotation=0, fontsize=25)
plt.yticks(fontsize=20)
plt.title("空气电台", fontsize=25)
plt.legend()
plt.savefig('不同人群的湿度平均值.png')
plt.show()

###########每类人群在不同日期pm2.5的平均值
datalist = sort(list(set(daytags)))
print(datalist)
dategroup = frame['PM2_5s'].groupby([frame['idtypes'], frame['daytags']]).mean()  #
dategroupstd = frame['PM2_5s'].groupby([frame['daytags']]).std()
###污染时长
dategrouptimetype = frame['deltatimes'].groupby([frame['idtypes'], frame['daytags'], frame['PM25types']]).sum()
dategrouptime = frame['deltatimes'].groupby([frame['idtypes'], frame['daytags']]).sum()

datagood25 = dategrouptimetype[:, :, '0良好']
# print(dategrouptime)
databad25 = dategrouptime - datagood25
# print(databad25)
###污染时长

####添加缺失值
idtypesmade = []
datesmade = []
for i in range(len(renqun)):
    for j in range(len(datalist)):
        idtypesmade.append(renqun[i])
        datesmade.append(datalist[j])

dfmade = {'idtypes': idtypesmade, 'daytags': datesmade}
dfmade['PM2_5s'] = np.zeros(len(renqun) * len(datalist))
dfmade = pd.DataFrame(dfmade)
dfinalmade = dfmade.set_index(['idtypes', 'daytags'])
dfinal = dategroup.reset_index().set_index(['idtypes', 'daytags'])
# print(dfinal)
# print(dfinalmade)

# dfadd = (dfinal+dfinalmade).fillna(0)
#####
# print(dfadd)
# print(dfadd.loc['学生'])
# print(list(dfadd.loc['学生']['PM2_5s']))
####按人群画图
xuesheng = list(dategroup.loc['学生'])
shinei = list(dategroup.loc['室内工作者'])
shiwai = list(dategroup.loc['室外工作者'])
zhufu = list(dategroup.loc['家庭主妇'])
####总体画图
total = list(dategroup)
# totalstd = list(dategroupstd)
# print(xuesheng)

# print(dfadd)
# print(list(dfadd))
# print(dategrouptime)

X = np.arange(len(datalist))[0:64]
t = np.array(total)
# ts = np.array(totalstd)
a = np.array(xuesheng)[0:64]
b = np.array(shiwai)[0:64]
c = np.array(shinei)[0:64]
d = np.array(zhufu)[0:64]
e = np.array([28.66666667, 21.33333333, 48.95833333, 50.29166667, 34.42307692, 41.79166667, 26.79166667, 35.33333333,
              68.54166667, 98.75, 37.53588517, 22.47851003,
              19.60674157, 23.65895954, 41.58333333, 76.83333333, 106.75, 91.375, 39.58333333, 17.45833333, 16.83333333,
              23.05, 28.90551181, 42.625, 47.625, 44.84210526,
              39.91666667, 26.68170426, 46.91666667, 49.46666667, 14.625, 73.625, 45.70833333, 67.54166667, 118.5338542,
              127.0416667, 71.19060052, 43.54, 48.66666667,
              63.08333333, 31.07552083, 37.41666667, 31.52380952, 41.20833333, 39.55, 40.12, 40.875, 29.16666667,
              29.66666667, 36.54166667, 52.87945205, 60.69565217,
              62.26902174, 51.16666667, 31.70833333, 22.79895561, 58.375, 60.7232376, 52.86956522, 59.79166667,
              69.45833333, 58.52173913, 61.75409836, 72.29166667])
fig = plt.gcf()  # ,74.75
fig.set_size_inches(18.5, 7)
# plt.plot(X,t,color="red", linewidth=2, linestyle="-",label = '总体')
# plt.errorbar(X, t, yerr=ts, fmt="o")
# print(len(X),len(a),len(b),len(c),len(d),len(e))
plt.plot(X, d, color="blue", linewidth=1, linestyle="-", label='家庭主妇')
plt.plot(X, a, color="red", linewidth=1, linestyle="-", label='学生')
plt.plot(X, c, color="green", linewidth=1, linestyle="-", label='室内工作者')
plt.plot(X, b, color="orange", linewidth=1, linestyle="-", label='室外工作者')
plt.plot(X, e, color="black", linewidth=2, linestyle="-", label='上海市天气')

plt.xlabel('日期', fontsize=20)
plt.ylabel('pm2.5平均值', fontsize=20)
s1 = pd.Series(t)  # 转为series类型
s2 = pd.Series(e)
corr = s1.corr(s2)  # 计算相关系数
print(corr)
plt.xticks(X, datalist, rotation=45, fontsize=12)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=20)
plt.savefig('结果图片\不同日期污染均值.png')
plt.show()

datalist = list(set(daytags))
datalist.sort()
dategroup = frame['PM2_5s'].groupby([frame['idtypes'], frame['daytags']]).mean()
###污染时长
dategrouptimetype = frame['deltatimes'].groupby([frame['idtypes'], frame['daytags'], frame['PM25types']]).sum()
dategrouptime = frame['deltatimes'].groupby([frame['idtypes'], frame['daytags']]).sum()

datagood25 = dategrouptimetype[:, :, '0良好']
# print(dategrouptime)
databad25 = dategrouptime - datagood25
# print(databad25)
###污染时长
print(databad25)
writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\污染时长.xlsx')
databad25.to_excel(writer, '污染时长')

writer.save()
xuesheng = list(databad25.loc['学生'])
shinei = list(databad25.loc['室内工作者'])
shiwai = list(databad25.loc['室外工作者'])
zhufu = list(databad25.loc['家庭主妇'])

# print(xuesheng)

# print(dfadd)
# print(list(dfadd))
# print(dategrouptime)

X = np.arange(len(datalist))[0:64]
base = np.ones(64)
a = np.array(xuesheng[0:64]) / 10
b = np.array(shiwai[0:64]) / 10
c = np.array(shinei[0:64]) / 10
d = np.array(zhufu[0:64]) / 10

fig = plt.gcf()
fig.set_size_inches(18.5, 7)
plt.plot(X, d, color="blue", linewidth=1, linestyle="-", label='家庭主妇')
plt.plot(X, a, color="red", linewidth=1, linestyle="-", label='学生')
plt.plot(X, c, color="green", linewidth=1, linestyle="-", label='室内工作者')
plt.plot(X, b, color="orange", linewidth=1, linestyle="-", label='室外工作者')
plt.plot(X, base, color="black", linewidth=1, linestyle="-")

plt.xlabel('日期', fontsize=20)
plt.ylabel('pm2.5污染时长', fontsize=20)

plt.xticks(X, datalist, rotation=0)
plt.yticks(fontsize=20)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=20)
plt.savefig('结果图片\不同日期污染时长.png')
plt.show()

# In[14]:


###########每类人群在不同日期温度的平均值

dategroup = frame['temperatures'].groupby([frame['idtypes'], frame['daytags']]).mean()  #
dategrouptime = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['ids'], frame['daytags'], frame['tempertypes']]).sum()
dategroupstd = frame['temperatures'].groupby([frame['daytags']]).std()
# datalist = ['518','519','520','521','522','523','524','525','526','527','528','529','530','531','601','602','603','604',
#             '605','606','607','608','609','610','611','612','613','614']

xuesheng = list(dategroup.loc['学生'])
shinei = list(dategroup.loc['室内工作者'])
shiwai = list(dategroup.loc['室外工作者'])
zhufu = list(dategroup.loc['家庭主妇'])
total = list(dategroup)
# print(xuesheng)

# print(dfadd)
# print(list(dfadd))
# print(dategrouptime)

totalstd = list(dategroupstd)
ts = np.array(totalstd)

X = np.arange(len(datalist))[0:64]
# t = np.array(total)
a = np.array(xuesheng)[0:64]
b = np.array(shiwai)[0:64]
c = np.array(shinei)[0:64]
d = np.array(zhufu)[0:64]
e = np.array(
    [22.4453125, 19.88932292, 22.22526042, 22.51041667, 23.53605769, 25.13541667, 25.29947917, 25.77083333, 27.26692708,
     26.41796875, 24.01435407, 24.0243553,
     23.32865169, 21.8583815, 23.47005208, 24.82161458, 25.11328125, 25.9609375, 23.70703125, 24.08463542, 21.78776042,
     21.6453125, 22.27559055, 22.59570313,
     23.42578125, 23.66052632, 24.61328125, 24.25062657, 24.38541667, 24.43125, 23.65820313, 24.66666667, 24.26171875,
     23.83984375, 24.80598958, 25.66927083,
     24.61357702, 24.765, 27.55078125, 28.08984375, 28.74479167, 29.08072917, 29.32440476, 29.63671875, 29.821875,
     31.18875, 31.06770833, 30.44140625, 30.01432292,
     30.08723958, 31.74383562, 32.38994565, 32.1263587, 32.23828125, 32.24739583, 32.43994778, 32.80859375, 32.68015666,
     33.45788043, 34.06770833, 34.27734375,
     34.10054348, 33.81693989, 33.74348958])  # ,32.7
fig = plt.gcf()
fig.set_size_inches(18.5, 7)
# plt.plot(X,t,color="red", linewidth=2, linestyle="-",label = '总体')
# plt.errorbar(X, t, yerr=ts, fmt="o")
plt.plot(X, d, color="blue", linewidth=1, linestyle="-", label='家庭主妇')
plt.plot(X, a, color="red", linewidth=1, linestyle="-", label='学生')
plt.plot(X, b, color="green", linewidth=1, linestyle="-", label='室外工作者')
plt.plot(X, c, color="orange", linewidth=1, linestyle="-", label='室内工作者')
plt.plot(X, e, color="black", linewidth=2, linestyle="-", label='上海市天气')

plt.xlabel('日期', fontsize=20)
plt.ylabel('温度平均值/℃', fontsize=20)
# s1=pd.Series(t) #转为series类型
# s2=pd.Series(e)
# corr=s1.corr(s2) #计算相关系数
# print(corr)
plt.xticks(X, datalist, rotation=45, fontsize=12)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=20)
plt.savefig('结果图片\不同日期温度均值.png')
plt.show()

# In[15]:


###########每类人群在不同日期湿度的平均值

dategroup = frame['humiditys'].groupby([frame['idtypes'], frame['daytags']]).mean()  #
dategrouptime = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['ids'], frame['daytags'], frame['humitypes']]).sum()
dategroupstd = frame['humiditys'].groupby([frame['daytags']]).std()
# datalist = ['518','519','520','521','522','523','524','525','526','527','528','529','530','531','601','602','603','604',
#             '605','606','607','608','609','610','611','612','613','614']

xuesheng = list(dategroup.loc['学生'])
shinei = list(dategroup.loc['室内工作者'])
shiwai = list(dategroup.loc['室外工作者'])
zhufu = list(dategroup.loc['家庭主妇'])

# print(xuesheng)

# print(dfadd)
# print(list(dfadd))
# print(dategrouptime)

# print(dategrouptime)

totalstd = list(dategroupstd)
ts = np.array(totalstd)

total = list(dategroup)
# t = np.array(total)
X = np.arange(len(datalist))[0:64]
a = np.array(xuesheng)[0:64]
b = np.array(shiwai)[0:64]
c = np.array(shinei)[0:64]
d = np.array(zhufu)[0:64]
e = np.array(
    [61.96520833, 83.3203125, 57.72135417, 62.19791667, 58.65384615, 55.27083333, 61.52864583, 73.19270833, 64.54947917,
     79.4453125, 51.20574163, 56.83094556, 60.57303371,
     82.4566474, 82.53125, 65.390625, 67.30208333, 71.95833333, 93.02604167, 77.984375, 85.72395833, 91.715625,
     78.61023622, 54.4140625, 63.58854167, 64.29210526, 72.47916667,
     90.28070175, 82.24479167, 88.96666667, 89.53515625, 87.49479167, 86.92708333, 93.51041667, 85.75260417,
     82.47395833, 83.82767624, 86.01, 80.390625, 83.9453125, 78.44270833,
     76.29166667, 70.50595238, 75.43229167, 73.69375, 66.97, 67.08072917, 67.46875, 74.2265625, 71.23958333,
     67.43835616, 63.60326087, 66.4673913, 66.87760417, 64.90104167,
     65.65796345, 67.9296875, 60.54308094, 57.66576087, 60.24479167, 64.140625, 65.58967391, 59.71584699,
     60.51822917])  # ,72.29
fig = plt.gcf()
fig.set_size_inches(18.5, 7)
# plt.plot(X,t,color="red", linewidth=2, linestyle="-",label = '总体')
# plt.errorbar(X, t, yerr=ts, fmt="o")
plt.plot(X, d, color="blue", linewidth=1, linestyle="-", label='家庭主妇')
plt.plot(X, a, color="red", linewidth=1, linestyle="-", label='学生')
plt.plot(X, b, color="green", linewidth=1, linestyle="-", label='室外工作者')
plt.plot(X, c, color="orange", linewidth=1, linestyle="-", label='室内工作者')
plt.plot(X, e, color="black", linewidth=2, linestyle="-", label='上海市天气')
# s1=pd.Series(t) #转为series类型
# s2=pd.Series(e)
# corr=s1.corr(s2) #计算相关系数
# print(corr)
plt.xlabel('日期', fontsize=20)
plt.ylabel('湿度平均值/%', fontsize=20)

plt.xticks(X, datalist, rotation=45, fontsize=12)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=20)
plt.savefig('结果图片\不同日期湿度均值.png')
plt.show()


# In[ ]:

########污染共有5个等级，污染1，污染2，污染3，污染4，污染5
########切换次数，主要针对pm2.5，共有6种切换方式，分别是切换次数：污染和非污染之间切换，切换1：切换开始是指从非污染变成污染1，结束是指污染1变成非污染
########切换2：切换开始是指从非污染变成污染2，切换结束是指污染2变成小于污染2，切换3：切换开始是指从非污染变成污染3，切换结束是指污染3变成小于污染3
########切换4：切换开始是指从非污染变成污染4，切换结束是指污染4变成小于污染4，切换5：切换开始是指从非污染变成污染5，切换结束是指污染5变成小于污染5
def get_changtime(id_num):
    # #print(idtypes)
    starttime = []
    stoptime = []
    everytime = []
    pm25type = []
    lasttime = 0
    idtype = 0
    rankstart = []
    rankstop = []
    whenchange = []
    hourchange = []
    when1 = []
    when2 = []
    hour1 = []
    hour2 = []
    #     starttime.append(lasttime)
    #     stoptime.append(lasttime)
    for i in range(len(id_nums)):
        if id_nums[i] == id_num:
            idtype = idtypes[i]
            week = weeklasts[i]
            hour = testtimes[i]
            # id_num = decive_ids_dict[id]
            if PM25types[i] != '0' and PM25types[i - 1] == '0':
                pm25type.append(PM25types[i])
                time1 = createtimes[i]
                starttime.append(time1)
                rankstart.append(i)
                when1.append(week)
                hour1.append(hour)
            elif PM25types[i] == '0' and PM25types[i - 1] != '0':
                pm25type.append(PM25types[i])
                time2 = createtimes[i]
                stoptime.append(time2)
                rankstop.append(i)
                when2.append(week)
                hour2.append(hour)
                #     #print(pm25type[0])
                #     if pm25type[0] != '0良好':
                #         stoptime.insert(0,starttime[0])

    print(len(stoptime), len(starttime), id_num)
    if len(stoptime) > 0 and len(starttime) > 0:
        if rankstop[0] >= rankstart[0]:
            if len(starttime) >= len(stoptime):
                for i in range(len(stoptime)):
                    time3 = stoptime[i] - starttime[i]
                    #         elif pm25type[0] != '0良好':
                    #             time3 = starttime[i]-stoptime[i-1]
                    time3 = time3.seconds / 3600
                    if time3 > 0.08:
                        everytime.append(time3)
                        lasttime += time3
                        whenchange.append(when1[i])
                        hourchange.append(hour1[i])
            else:
                for i in range(len(starttime)):
                    time3 = stoptime[i] - starttime[i]
                    #         elif pm25type[0] != '0良好':
                    #             time3 = starttime[i]-stoptime[i-1]
                    time3 = time3.seconds / 3600
                    if time3 > 0.08:
                        everytime.append(time3)
                        lasttime += time3
                        whenchange.append(when1[i])
                        hourchange.append(hour1[i])
        else:
            for i in range(1, len(starttime)):
                time3 = stoptime[i] - starttime[i - 1]
                #         elif pm25type[0] != '0良好':
                #             time3 = starttime[i]-stoptime[i-1]
                time3 = time3.seconds / 3600
                if time3 > 0.08:
                    everytime.append(time3)
                    whenchange.append(when1[i - 1])
                    hourchange.append(hour1[i - 1])
                    lasttime += time3
        return id_num, idtype, lasttime, len(everytime), everytime, whenchange, hourchange
    else:
        return id_num, idtype, lasttime, len(everytime), everytime, whenchange, hourchange


# 增加停留时间
def get_changtime1(id_num, rank):
    # #print(idtypes)
    starttime = []
    stoptime = []
    everytime = []
    pm25type = []
    lasttime = 0
    idtype = 0
    rankstart = []
    rankstop = []
    whenchange = []
    hourchange = []
    when1 = []
    when2 = []
    hour1 = []
    hour2 = []
    #     starttime.append(lasttime)
    #     stoptime.append(lasttime)
    for i in range(len(id_nums)):
        if id_nums[i] == id_num:
            idtype = idtypes[i]
            week = weeklasts[i]
            hour = testtimes[i]
            # id_num = decive_ids_dict[id]
            if int(PM25types[i]) == rank and PM25types[i - 1] == '0':
                pm25type.append(PM25types[i])
                time1 = createtimes[i]
                starttime.append(time1)
                rankstart.append(i)
                when1.append(week)
                hour1.append(hour)
            elif int(PM25types[i]) < rank and int(PM25types[i - 1]) >= rank:
                pm25type.append(PM25types[i])
                time2 = createtimes[i]
                rankstop.append(i)
                stoptime.append(time2)
                when2.append(week)
                hour2.append(hour)
                #     #print(pm25type[0])
                #     if pm25type[0] != '0良好':
                #         stoptime.insert(0,starttime[0])
                #         该算法有一个问题，结束点会比开始点多，解决办法如下：
                #         将结束点中的数据减去开始点中的数据，取其中差值最小的点作为真正的结束点

    chazhilist = []
    rankstop_xz = []
    stoptime_xz = []
    if len(rankstop) > 0 and len(rankstart) > 0:
        if rankstop[0] >= rankstart[0]:
            if rankstop[-1] >= rankstart[-1]:
                for i in range(len(rankstart)):
                    chazhis = []
                    for j in range(len(rankstop)):
                        chazhis.append(rankstop[j] - rankstart[i])
                    minchazhi = 10000
                    for p in chazhis:
                        if abs(p) < abs(minchazhi) and p > 0:
                            minchazhi = p
                    chazhilist.append(minchazhi)
                for i in range(len(starttime)):
                    rankstop_xz.append(rankstart[i] + chazhilist[i])
                    stoptime_xz.append(createtimes[rankstart[i] + chazhilist[i]])
            else:
                for i in range(len(rankstart) - 1):
                    chazhis = []
                    for j in range(len(rankstop)):
                        chazhis.append(rankstop[j] - rankstart[i])
                    minchazhi = 10000
                    for p in chazhis:
                        if abs(p) < abs(minchazhi) and p > 0:
                            minchazhi = p
                    chazhilist.append(minchazhi)
                for i in range(len(starttime) - 1):
                    rankstop_xz.append(rankstart[i] + chazhilist[i])
                    stoptime_xz.append(createtimes[rankstart[i] + chazhilist[i]])
                    # #print(chazhis)
                    # #print(minchazhi)


        else:
            for i in range(len(rankstart)):
                chazhis = []
                for j in range(1, len(rankstop)):
                    chazhis.append(rankstop[j] - rankstart[i])
                    # chazhismin = max(chazhis)
                minchazhi = 10000
                for p in chazhis:
                    if abs(p) < abs(minchazhi) and p > 0:
                        minchazhi = p
                chazhilist.append(minchazhi)
            for i in range(len(rankstart)):
                rankstop_xz.append(rankstart[i] + chazhilist[i])
                stoptime_xz.append(createtimes[rankstart[i] + chazhilist[i]])
        print(chazhilist)
        print(rankstop_xz)
        print(len(stoptime_xz))
        print(len(starttime))

    if len(stoptime_xz) > 0 and len(starttime) > 0:
        if rankstop_xz[0] >= rankstart[0]:
            # #print(len(stoptime_xz))
            # #print(len(starttime))
            # #print(idtype)
            # #print(id_num)
            # #print(rankstart)
            # #print(rankstop)
            for i in range(len(stoptime_xz)):
                time3 = stoptime_xz[i] - starttime[i]
                #         elif pm25type[0] != '0良好':
                #             time3 = starttime[i]-stoptime_xz[i-1]
                time3 = time3.seconds / 3600
                if time3 > 0.08:
                    everytime.append(time3)
                    lasttime += time3
                    whenchange.append(when1[i])
                    hourchange.append(hour1[i])
        else:
            if len(stoptime_xz) > 1:
                for i in range(1, len(starttime)):
                    time3 = stoptime_xz[i] - starttime[i - 1]
                    #         elif pm25type[0] != '0良好':
                    #             time3 = starttime[i]-stoptime_xz[i-1]
                    time3 = time3.seconds / 3600
                    if time3 > 0.08:
                        everytime.append(time3)
                        whenchange.append(when1[i - 1])
                        hourchange.append(hour1[i - 1])
                        lasttime += time3
        return id_num, idtype, lasttime, len(everytime), everytime, whenchange, hourchange
    else:
        return id_num, idtype, lasttime, len(everytime), everytime, whenchange, hourchange


#######每类人群处于不同污染等级中时长的绝对值

renqungrouped25 = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['PM25types'], frame['weeklasts']]).sum().reset_index()
rengrouped25 = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['PM25types'], frame['weeklasts']]).sum()
rengrouped25test = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['PM25types'], frame['testdays']]).sum()
rengrouped25test_3 = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['PM25types'], frame['testday_3ds']]).sum()

rengrouped25_8hour = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['PM25types'], frame['testtimes']]).sum()

rengrouped25 = rengrouped25.reset_index()
rengrouped25test = rengrouped25test.reset_index()
rengrouped25test_3 = rengrouped25test_3.reset_index()
meangroup = rengrouped25['deltatimes'].groupby(
    [rengrouped25['idtypes'], rengrouped25['PM25types'], rengrouped25['weeklasts']]).mean().reset_index()
stdgroup = rengrouped25['deltatimes'].groupby(
    [rengrouped25['idtypes'], rengrouped25['PM25types'], rengrouped25['weeklasts']]).std().reset_index()
# print(stdgroup)
print(meangroup)
# print(len(meangroup))
writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\output.xlsx')
rengrouped25.to_excel(writer, '污染时长绝对值')
rengrouped25test.to_excel(writer, '污染时长绝对值test')
rengrouped25test_3.to_excel(writer, '污染时长绝对值_3test')
rengrouped25_8hour.to_excel(writer, '污染时长绝对值_8hour')
writer.save()

piclist25mean = list(meangroup['deltatimes'])
piclist25std = list(stdgroup['deltatimes'])
zhufu = []
shinei = []
shiwai = []
xuesheng = []
for j in range(1, 6):
    xuesheng.append(piclist25mean[0 + j])
    shinei.append(piclist25mean[1 * 6 + j])
    shiwai.append(piclist25mean[2 * 6 + j])
    zhufu.append(piclist25mean[3 * 6 + j])

zhufu1 = []
shinei1 = []
shiwai1 = []
xuesheng1 = []
for j in range(1, 6):
    xuesheng1.append(piclist25std[0 + j])
    shinei1.append(piclist25std[1 * 6 + j])
    shiwai1.append(piclist25std[2 * 6 + j])
    zhufu1.append(piclist25std[3 * 6 + j])

size = 5
x = np.arange(size)
a = np.array(zhufu)
stda = np.array(zhufu1)
b = np.array(shinei)
stdb = np.array(shinei1)
c = np.array(shiwai)
stdc = np.array(shiwai1)
d = np.array(xuesheng)
stdd = np.array(xuesheng1)

total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / 3
fig = plt.gcf()
fig.set_size_inches(18.5, 7)
plt.bar(x, a, width=width, label='家庭主妇')
plt.errorbar(x, a, yerr=stda, fmt="o")
plt.bar(x + width, b, width=width, label='室内工作者')
plt.errorbar(x + width, b, yerr=stdb, fmt="o")
plt.bar(x + 2 * width, c, width=width, label='室外工作者')
plt.errorbar(x + 2 * width, c, yerr=stdc, fmt="o")

plt.bar(x + 3 * width, d, width=width, label='学生')
plt.errorbar(x + 3 * width, d, yerr=stdd, fmt="o")

plt.xlabel('空气污染等级', fontsize=20)
plt.ylabel('平均总时长/小时', fontsize=25)
label = ['轻度污染', '中度污染', '重度污染', '严重污染', '超严重污染']
plt.xticks(x, label, rotation=0, fontsize=20)
plt.yticks(fontsize=20)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=15)
plt.savefig('结果图片\不同人群的污染时长.png')
plt.show()

##########每类人群处于不同污染等级中时长的相对值


# 获取每个人总共的时长
rengrouped25total = rengrouped25['deltatimes'].groupby(
    [rengrouped25['idtypes'], rengrouped25['id_nums'], rengrouped25['weeklasts']]).sum().reset_index()
##获取每个人污染时长占比
addrengrouped25 = pd.merge(rengrouped25, rengrouped25total, on=['idtypes', 'id_nums', 'weeklasts'], how='left')
addrengrouped25['zhanbigrouped'] = addrengrouped25['deltatimes_x'] / addrengrouped25['deltatimes_y']

####获取测试当天及测试前三天的时长占比

rengrouped25totaltest = rengrouped25test['deltatimes'].groupby(
    [rengrouped25test['idtypes'], rengrouped25test['id_nums'], rengrouped25test['testdays']]).sum().reset_index()
addrengrouped25test = pd.merge(rengrouped25test, rengrouped25totaltest, on=['idtypes', 'id_nums', 'testdays'],
                               how='left')
addrengrouped25test['zhanbigrouped'] = addrengrouped25test['deltatimes_x'] / addrengrouped25test['deltatimes_y']

rengrouped25totaltest_3 = rengrouped25test_3['deltatimes'].groupby(
    [rengrouped25test_3['idtypes'], rengrouped25test_3['id_nums'],
     rengrouped25test_3['testday_3ds']]).sum().reset_index()
addrengrouped25test_3 = pd.merge(rengrouped25test_3, rengrouped25totaltest_3, on=['idtypes', 'id_nums', 'testday_3ds'],
                                 how='left')
addrengrouped25test_3['zhanbigrouped'] = addrengrouped25test_3['deltatimes_x'] / addrengrouped25test_3['deltatimes_y']

rengrouped25_8hour = rengrouped25_8hour.reset_index()
rengrouped25total_8hour = rengrouped25_8hour['deltatimes'].groupby(
    [rengrouped25_8hour['idtypes'], rengrouped25_8hour['id_nums'], rengrouped25_8hour['testtimes']]).sum().reset_index()
addrengrouped25_8hour = pd.merge(rengrouped25_8hour, rengrouped25total_8hour, on=['idtypes', 'id_nums', 'testtimes'],
                                 how='left')
addrengrouped25_8hour['zhanbigrouped'] = addrengrouped25_8hour['deltatimes_x'] / addrengrouped25_8hour['deltatimes_y']

# rengrouped25_8hour = frame['deltatimes'].groupby([frame['idtypes'],frame['id_nums'],frame['PM25types'],frame['testtimes']]).sum()
# rengrouped25_8hour.to_excel(writer,'污染时长绝对值_8hour')

# print(addrengrouped25)
# print(type(addrengrouped25))
writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\每个人污染时长占比1.xlsx')
addrengrouped25.to_excel(writer, '每个人污染时长占比')
addrengrouped25test.to_excel(writer, '每个人污染时长占比test')
addrengrouped25test_3.to_excel(writer, '每个人污染时长占比test_3')
addrengrouped25_8hour.to_excel(writer, '每个人污染时长占比8hour')
writer.save()
###获取人群污染时长占比平均值和标准差
# addrengrouped25 = addrengrouped25.reset_index()
addrengrouped25mean = addrengrouped25['zhanbigrouped'].groupby(
    [addrengrouped25['idtypes'], addrengrouped25['PM25types']]).mean()
addrengrouped25std = addrengrouped25['zhanbigrouped'].groupby(
    [addrengrouped25['idtypes'], addrengrouped25['PM25types']]).std()

addgrouped25['zhanbigrouped'] = addgrouped25['deltatimes_x'] / addgrouped25['deltatimes_y']
# print(addgrouped25)
fig2 = plt.gcf()
fig2.set_size_inches(18.5, 7)
piclist = list(addrengrouped25mean)
print(piclist)
zhufu = []
shinei = []
shiwai = []
xuesheng = []
for j in range(1, 6):
    xuesheng.append(piclist[0 + j])
    shinei.append(piclist[1 * 6 + j])
    shiwai.append(piclist[2 * 6 + j])
    zhufu.append(piclist[3 * 6 + j])
# print(xuesheng,shinei,shiwai,zhufu)

piclist25std = list(addrengrouped25std)
zhufu1 = []
shinei1 = []
shiwai1 = []
xuesheng1 = []
for j in range(1, 6):
    xuesheng1.append(piclist25std[0 + j])
    shinei1.append(piclist25std[1 * 6 + j])
    shiwai1.append(piclist25std[2 * 6 + j])
    zhufu1.append(piclist25std[3 * 6 + j])

size = 5
x = np.arange(size)
a = np.array(zhufu)
stda = np.array(zhufu1)
b = np.array(shinei)
stdb = np.array(shinei1)
c = np.array(shiwai)
stdc = np.array(shiwai1)
d = np.array(xuesheng)
stdd = np.array(xuesheng1)

total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / 3
fig = plt.gcf()
fig.set_size_inches(18.5, 7)
plt.bar(x, a, width=width, label='家庭主妇')
plt.errorbar(x, a, yerr=stda, fmt="o")
plt.bar(x + width, b, width=width, label='室内工作者')
plt.errorbar(x + width, b, yerr=stdb, fmt="o")
plt.bar(x + 2 * width, c, width=width, label='室外工作者')
plt.errorbar(x + 2 * width, c, yerr=stdc, fmt="o")
plt.bar(x + 3 * width, d, width=width, label='学生')
plt.errorbar(x + 3 * width, d, yerr=stdd, fmt="o")
plt.xlabel('空气污染等级', fontsize=20)
plt.ylabel('平均占所有时长的比例', fontsize=25)
label = ['轻度污染', '中度污染', '重度污染', '严重污染', '超严重污染']
plt.xticks(x, label, rotation=0, fontsize=20)
plt.yticks(fontsize=20)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=15)
plt.savefig('结果图片\不同人群的污染时长占比.png')
plt.show()

# In[12]:


###########每类人群处于不同湿度等级中时长的绝对值

renqungroupedhum = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['humitypes'], frame['weeklasts']]).sum().reset_index()
renqungrouped = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['weeklasts']]).sum().reset_index()
addgroupedhum = pd.merge(renqungroupedhum, renqungrouped, on=['idtypes', 'id_nums', 'weeklasts'], how='left')
addgroupedhum['zhanbigrouped'] = addgroupedhum['deltatimes_x'] / addgroupedhum['deltatimes_y']
piclisthum = list(addgroupedhum['deltatimes_x'])
# print(addgrouped)
# print(piclist)
####获取测试当天及测试前三天的时长占比外加8小时
renqungroupedhumtest = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['humitypes'], frame['testdays']]).sum().reset_index()
renqungroupedtest = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testdays']]).sum().reset_index()
addgroupedhumtest = pd.merge(renqungroupedhumtest, renqungroupedtest, on=['idtypes', 'id_nums', 'testdays'], how='left')
addgroupedhumtest['zhanbigrouped'] = addgroupedhumtest['deltatimes_x'] / addgroupedhumtest['deltatimes_y']

renqungroupedhumtest_3 = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['humitypes'], frame['testday_3ds']]).sum().reset_index()
renqungroupedtest_3 = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testday_3ds']]).sum().reset_index()
addgroupedhumtest_3 = pd.merge(renqungroupedhumtest_3, renqungroupedtest_3, on=['idtypes', 'id_nums', 'testday_3ds'],
                               how='left')
addgroupedhumtest_3['zhanbigrouped'] = addgroupedhumtest_3['deltatimes_x'] / addgroupedhumtest_3['deltatimes_y']

renqungroupedhum_8hour = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['humitypes'], frame['testtimes']]).sum().reset_index()
renqungrouped_8hour = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testtimes']]).sum().reset_index()
addgroupedhum_8hour = pd.merge(renqungroupedhum_8hour, renqungrouped_8hour, on=['idtypes', 'id_nums', 'testtimes'],
                               how='left')
addgroupedhum_8hour['zhanbigrouped'] = addgroupedhum_8hour['deltatimes_x'] / addgroupedhum_8hour['deltatimes_y']

writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\每个人湿度时长占比1.xlsx')
addgroupedhum.to_excel(writer, '每个人湿度时长占比')
addgroupedhumtest.to_excel(writer, '每个人湿度时长占比test')
addgroupedhumtest_3.to_excel(writer, '每个人湿度时长占比test_3')
addgroupedhum_8hour.to_excel(writer, '每个人湿度时长占比8hour')

writer.save()
zhufu = []
shinei = []
shiwai = []
xuesheng = []
for j in range(3):
    xuesheng.append(piclisthum[0 + j])
    shinei.append(piclisthum[1 * 3 + j])
    shiwai.append(piclisthum[2 * 3 + j])
    zhufu.append(piclisthum[3 * 3 + j])
print(xuesheng, shinei, shiwai, zhufu)
size = 3
x = np.arange(size)
a = np.array(zhufu)
b = np.array(shiwai)
c = np.array(shinei)
d = np.array(xuesheng)

total_width, n = 0.8, 5
width = total_width / n
x = x - (total_width - width) / 2
fig = plt.gcf()
fig.set_size_inches(18.5, 7)
plt.bar(x - width, a, width=width, label='家庭主妇')
plt.bar(x, b, width=width, label='室外工作者')
plt.bar(x + width, c, width=width, label='室内工作者')
plt.bar(x + 2 * width, d, width=width, label='学生')
plt.xlabel('湿度等级', fontsize=15)
plt.ylabel('总时长/小时', fontsize=15)
label = ['偏干', '适中', '偏湿']
plt.xticks(x, label, rotation=0, fontsize=15)
plt.yticks(fontsize=15)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=15)
plt.savefig('结果图片\不同人群不同湿度时长.png')
plt.show()

# In[13]:


#######每类人群处于不同温度等级中时长的绝对值

renqungroupedtep = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['tempertypes'], frame['weeklasts']]).sum().reset_index()
renqungrouped = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['weeklasts']]).sum().reset_index()
addgroupedtep = pd.merge(renqungroupedtep, renqungrouped, on=['idtypes', 'id_nums', 'weeklasts'], how='left')
addgroupedtep['zhanbigrouped'] = addgroupedtep['deltatimes_x'] / addgroupedtep['deltatimes_y']
piclisttep = list(addgroupedtep['deltatimes_x'])

# print(addgrouped)
# print(piclist)

####获取测试当天及测试前三天的时长占比外加8小时
renqungroupedteptest = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['tempertypes'], frame['testdays']]).sum().reset_index()
renqungroupedtest = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testdays']]).sum().reset_index()
addgroupedteptest = pd.merge(renqungroupedteptest, renqungroupedtest, on=['idtypes', 'id_nums', 'testdays'], how='left')
addgroupedteptest['zhanbigrouped'] = addgroupedteptest['deltatimes_x'] / addgroupedteptest['deltatimes_y']

renqungroupedteptest_3 = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['tempertypes'], frame['testday_3ds']]).sum().reset_index()
renqungroupedtest_3 = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testday_3ds']]).sum().reset_index()
addgroupedteptest_3 = pd.merge(renqungroupedteptest_3, renqungroupedtest_3, on=['idtypes', 'id_nums', 'testday_3ds'],
                               how='left')
addgroupedteptest_3['zhanbigrouped'] = addgroupedteptest_3['deltatimes_x'] / addgroupedteptest_3['deltatimes_y']

renqungroupedtep_8hour = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['tempertypes'], frame['testtimes']]).sum().reset_index()
renqungrouped_8hour = frame['deltatimes'].groupby(
    [frame['idtypes'], frame['id_nums'], frame['testtimes']]).sum().reset_index()
addgroupedtep_8hour = pd.merge(renqungroupedtep_8hour, renqungrouped_8hour, on=['idtypes', 'id_nums', 'testtimes'],
                               how='left')
addgroupedtep_8hour['zhanbigrouped'] = addgroupedtep_8hour['deltatimes_x'] / addgroupedtep_8hour['deltatimes_y']

writer = pd.ExcelWriter(r'C:\Users\stacy\Desktop\每个人温度时长占比1.xlsx')
addgroupedtep.to_excel(writer, '每个人温度时长占比')
addgroupedteptest.to_excel(writer, '每个人温度时长占比test')
addgroupedteptest_3.to_excel(writer, '每个人温度时长占比test_3')
addgroupedtep_8hour.to_excel(writer, '每个人温度时长占比8hour')
writer.save()

zhufu = []
shinei = []
shiwai = []
xuesheng = []

for j in range(10):
    xuesheng.append(piclisttep[0 + j])
    shinei.append(piclisttep[1 * 10 + j])
    shiwai.append(piclisttep[2 * 10 + j])
    zhufu.append(piclisttep[3 * 10 + j])
print(xuesheng, shinei, shiwai, zhufu)
size = 10
x = np.arange(size)
a = np.array(zhufu)
b = np.array(shiwai)
c = np.array(shinei)
d = np.array(xuesheng)

total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / 3
fig = plt.gcf()
fig.set_size_inches(18.5, 7)
plt.bar(x - width, a, width=width, label='家庭主妇')
plt.bar(x, b, width=width, label='室外工作者')
plt.bar(x + width, c, width=width, label='室内工作者')
plt.bar(x + 2 * width, d, width=width, label='学生')
plt.xlabel('温度等级', fontsize=15)
plt.ylabel('总时长/小时', fontsize=15)

label = ['暖1', '暖2', '热1', '热2', '热3', '热4', '热5', '热6', '热7', '热8']
plt.xticks(x, label, rotation=0, fontsize=15)
plt.yticks(fontsize=15)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=15)

plt.savefig('结果图片\不同人群不同温度时长.png')
plt.show()


# In[ ]:



##########每类人群处于不同污染等级中时长的相对值----饼图
def drawpierenqun(list, renqun):
    labels = '1', '2', '', '', '', ''
    fracs = list
    print(len(fracs))
    explode = [0.1] * len(list)  # 0.1 凸出这部分，
    plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
    # autopct ，show percet
    plt.pie(x=fracs, labels=labels, explode=explode,  # autopct='%1.1f %%',
            shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6  # ,patches.p_texts =renqun

            )
    '''
    labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
    autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
    shadow，饼是否有阴影
    startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
    pctdistance，百分比的text离圆心的距离
    patches, p_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
    '''
    plt.savefig('结果图片\饼图' + renqun + '.png')
    plt.show()


def drawpieshebei(lists, r):
    plt.figure(figsize=(6, 9))
    # 定义饼状图的标签，标签是列表
    #     labels = [u'第一部分',u'第二部分',u'第三部分']
    labels = list(range(1, len(lists) + 1))
    #     labels = '空气良好', '污染', '', '','',''
    colors = ['lightgreen', 'red', 'red', 'red', 'red', 'red']
    fracs = lists
    explode = [0] * len(lists)  # 0.1 凸出这部分，
    plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
    # autopct ，show percet
    patches, l_text = plt.pie(x=fracs, explode=explode,  # colors = colors,#autopct='%1.1f %%',
                              shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6)

    #     plt.pie(x=fracs, labels=labels, explode=explode,#autopct='%1.1f %%',
    #             shadow=True, labeldistance=1.1, startangle = 90,pctdistance = 0.6#,patches.p_texts =renqun

    #             )
    '''
    labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
    autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
    shadow，饼是否有阴影
    startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
    pctdistance，百分比的text离圆心的距离
    patches, p_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
    '''
    for t in l_text:
        t.set_size = (50)
    # for t in p_text:
    #         t.set_size=(20)
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal', fontsize=30)
    #     plt.legend()
    plt.savefig('结果图片\饼图' + r + '.png')
    plt.show()


def showpie():
    zhufu = list(shebeigrouped25.loc['家庭主妇']['zhanbigrouped'])
    shinei = list(shebeigrouped25.loc['室内工作者']['zhanbigrouped'])
    shiwai = list(shebeigrouped25.loc['室外工作者']['zhanbigrouped'])
    xuesheng = list(shebeigrouped25.loc['学生']['zhanbigrouped'])

    drawpieshebei(xuesheng, '学生')
    drawpieshebei(shinei, '室内工作者')
    drawpieshebei(shiwai, '室外工作者')
    drawpieshebei(zhufu, '家庭主妇')


def showpieor(datalist):
    zhufu = []
    shinei = []
    shiwai = []
    xuesheng = []
    for j in range(6):
        xuesheng.append(piclist[0 + j])
        shinei.append(piclist[1 * 6 + j])
        shiwai.append(piclist[2 * 6 + j])
        zhufu.append(piclist[3 * 6 + j])

    drawpieshebei(xuesheng, '学生1')
    drawpieshebei(shinei, '室内工作者1')
    drawpieshebei(shiwai, '室外工作者1')
    drawpieshebei(zhufu, '家庭主妇1')


shebeigrouped25 = frame['deltatimes'].groupby([frame['idtypes'], frame['id_nums'], frame['wurantypes']]).sum()

shebeigrouped25 = shebeigrouped25[:, :, '1'].reset_index()
hhgrouped = frame['deltatimes'].groupby([frame['idtypes'], frame['wurantypes']]).sum()

hhgrouped = hhgrouped[:, '1'].reset_index()
# print(hh)

print(hhgrouped)
shebeigrouped25 = pd.merge(shebeigrouped25, hhgrouped, on=['idtypes'], how='left')

shebeigrouped25['zhanbigrouped'] = shebeigrouped25['deltatimes_x'] / shebeigrouped25['deltatimes_y']
shebeigrouped25 = shebeigrouped25.set_index('idtypes', 'id_nums')

print(list(shebeigrouped25.loc['学生']['zhanbigrouped']))
# shebeipiclist = list(shebeigrouped25['zhanbigrouped'])

# print(shebeigrouped25)
# print(shebeigrouped25['学生'])
# print(shebeigrouped25['室内工作者'])
# print(shebeigrouped25['室外工作者'])
# print(shebeigrouped25['家庭主妇'])
print(shebeigrouped25)
# showpieor(piclist)
# showpie()


# In[22]:


###########每类人群处于不同湿度等级中时长的相对值

fig2 = plt.gcf()
fig2.set_size_inches(18.5, 7)
piclist = list(addgroupedhum['zhanbigrouped'])
zhufu = []
shinei = []
shiwai = []
xuesheng = []
for j in range(3):
    xuesheng.append(piclist[0 + j])
    shinei.append(piclist[1 * 3 + j])
    shiwai.append(piclist[2 * 3 + j])
    zhufu.append(piclist[3 * 3 + j])
print(xuesheng, shinei, shiwai, zhufu)
size = 3
x = np.arange(size)
a = np.array(zhufu)
b = np.array(shiwai)
c = np.array(shinei)
d = np.array(xuesheng)

total_width, n = 0.8, 5
width = total_width / n
x = x - (total_width - width) / 2
fig = plt.gcf()
fig.set_size_inches(18.5, 7)
plt.bar(x - width, a, width=width, label='家庭主妇')
plt.bar(x, b, width=width, label='室外工作者')
plt.bar(x + width, c, width=width, label='室内工作者')
plt.bar(x + 2 * width, d, width=width, label='学生')
plt.xlabel('湿度等级', fontsize=15)
plt.ylabel('相对总时长占比', fontsize=15)
label = ['偏干', '适中', '偏湿']
plt.xticks(x, label, rotation=0, fontsize=15)
plt.yticks(fontsize=15)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=15)
plt.savefig('结果图片\不同人群不同湿度时长相对值.png')
plt.show()

# In[21]:


#######每类人群处于不同温度等级中时长的相对值

fig2 = plt.gcf()
fig2.set_size_inches(18.5, 7)
piclist = list(addgroupedtep['zhanbigrouped'])
zhufu = []
shinei = []
shiwai = []
xuesheng = []

for j in range(10):
    xuesheng.append(piclist[0 + j])
    shinei.append(piclist[1 * 10 + j])
    shiwai.append(piclist[2 * 10 + j])
    zhufu.append(piclist[3 * 10 + j])
print(xuesheng, shinei, shiwai, zhufu)
size = 10
x = np.arange(size)
a = np.array(zhufu)
b = np.array(shiwai)
c = np.array(shinei)
d = np.array(xuesheng)

total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / 3
fig = plt.gcf()
fig.set_size_inches(18.5, 7)
plt.bar(x - width, a, width=width, label='家庭主妇')
plt.bar(x, b, width=width, label='室外工作者')
plt.bar(x + width, c, width=width, label='室内工作者')
plt.bar(x + 2 * width, d, width=width, label='学生')
plt.xlabel('温度等级', fontsize=15)
plt.ylabel('相对总时长占比', fontsize=15)

label = ['暖1', '暖2', '热1', '热2', '热3', '热4', '热5', '热6', '热7', '热8']
plt.xticks(x, label, rotation=0, fontsize=15)
plt.yticks(fontsize=15)
plt.title("空气电台", fontsize=25)
plt.legend(fontsize=15)
plt.savefig('结果图片\不同人群不同温度时长相对值.png')
plt.show()

