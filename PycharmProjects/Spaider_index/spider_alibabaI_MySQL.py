# -*- coding:utf-8 -*-
import urllib, urllib.request
import re
import xlwt, time, xlrd
from bs4 import BeautifulSoup
import sys
import simplejson
import datetime
import pymysql

# from datetimeshz import date_time
# 连接服务器
db = pymysql.connect("localhost", "root", "qwer1234", "skin_database", charset="utf8")
cursor = db.cursor()
sql = '''replace into ali_index(关键字,日期,淘宝指数,淘宝同比上周,1688采购指数,1688采购同比上周,1688供应指数,1688供应同比上周)
values
(%s,%s,%s,%s,%s,%s,%s,%s)'''
title = ['淘宝指数', '同比上周', '1688采购指数', '同比上周', '1688供应指数', '同比上周']
with open(r'./keyword.txt') as f:
    searchList = f.readlines()
dictList = {'BB霜': '97,821,011,043,093', '彩妆套装': '97,821,011,043,094', '唇笔': '97,821,011,043,504',
            '唇彩': '97,821,011,034,783',
            '口红': '97,821,011,034,783', '粉饼': '97,821,011,040,898', '粉底液': '97,821,011,034,785',
            '隔离霜': '97,821,011,046,942',
            '睫毛膏': '97,821,011,034,780', '眉笔': '97,821,011,034,779', '蜜粉': '97,821,011,040,900',
            '腮红': '97,821,011,034,784',
            '香水': '978,210,182,105', '眼线笔': '97,821,011,036,812', '眼影': '97,82101,1034782', '遮瑕笔': '97,82101,1043095',
            '唇膜': '97,1043498,1043500', '润唇膏': '97,1043498,1043499', '甲油胶': '97,1043162,124150002',
            '假指甲': '97,1043162,1043166',
            '美甲笔': '97,1043162,124186007', '美甲工具套装': '97,1043162,1043168', '美甲器': '97,1043162,1043169',
            '卸甲用品': '97,1043162,124256002', '指甲锉': '97,1043162,1043164', '指甲剪': '97,1043162,1043163',
            '指甲刷': '97,1043162,1043165', '指甲贴': '97,1043162,1043167', '指甲油': '97,1043162,1034781',
            '粉刺针': '97,1043171,1043178',
            '粉扑': '97,1043171,1043179', '化妆工具套装': '97,1043171,1043188', '化妆棉': '97,1043171,1043183',
            '化妆刷': '97,1043171,1043184', '假睫毛': '97,1043171,1043174', '睫毛夹': '97,1043171,1043176',
            '洁面仪': '97,1043171,122668001',
            '卷发球': '97,1043171,1043145', '眉刀': '97,1043171,1043177', '美发剪': '97,1043171,1043144',
            '美发梳': '97,1043171,1043143',
            '美容棒': '97,1043171,123702001', '美容导入仪': '97,1043171,123698002', '美眼仪': '97,1043171,123696003',
            '面膜纸': '97,1043171,1043181', '瘦脸工具': '97,1043171,123696002', '双眼皮贴': '97,1043171,1043175',
            '吸油面纸': '97,1043171,1043185', 'T区护理': '97,1042634,1043436', '防晒霜': '97,1042634,1034761',
            '化妆水': '97,1042634,1034766', '洁面产品': '97,1042634,1042655', '面部按摩霜': '97,1042634,1043434',
            '面部护理套装': '97,1042634,1036807', '面部精华': '97,1042634,1043433', '面部精油': '97,1042634,123854001',
            '面部磨砂': '97,1042634,1043435', '面膜': '97,1042634,1034765', '面霜': '97,1042634,1034763',
            '乳液': '97,1042634,1034762',
            '手工皂': '97,1042634,122708002', '卸妆产品': '97,1042634,1041750', '眼部护理': '97,1042634,121708002',
            '男士洁面': '97,121702001,121706001', '男士护理套装': '97,121702001,122310013', '男士面部精华': '97,121702001,121694002',
            '男士面膜': '97,121702001,121710002', '男士乳液': '97,121702001,121710001', '男士润唇膏': '97,121702001,121714001',
            '男士身体护理': '97,121702001,122364006', '男士爽肤水': '97,121702001,121708001', '男士眼霜': '97,121702001,121712001',
            '剃须膏': '97,121702001,1034770', '颈部护理': '97,126182004,1046969', '身体精油': '97,126182004,1041576',
            '身体乳': '97,126182004,1043070', '手部护理': '97,126182004,1034758', '纹绣产品': '97,126182004,126136006',
            '纤体膏': '97,126182004,1034565', '胸部护理': '97,126182004,1034566', '冻干粉': '97,123650003,123650004',
            '花水纯露': '97,123650003,123666002', '美容胶囊': '97,123650003,123666003', '原液': '97,123650003,123646004',
            '专业线精油': '97,123650003,124774001', '假牙清洁': '130822220,122268004,123662003',
            '口腔清新剂': '130822220,122268004,122282004', '漱口水': '130822220,122268004,122220009',
            '牙齿美白笔': '130822220,122268004,122706001', '牙齿美白套装': '130822220,122268004,122702002',
            '牙粉': '130822220,122268004,122192009', '牙膏': '130822220,122268004,122216007',
            '牙刷': '130822220,122268004,10317',
            '发膜': '130822220,10313,1047068', '护发精油': '130822220,10313,1034776', '护发素': '130822220,10313,1047066',
            '奶疗素': '130822220,10313,122204003', '染发工具': '130822220,10313,122774001', '染发剂': '130822220,10313,1034771',
            '烫发剂': '130822220,10313,1034772', '洗发护发套装': '130822220,10313,1047070', '洗发水': '130822220,10313,1047065',
            '育发剂': '130822220,10313,1034773', '搓泥浴宝': '130822220,1043058,122284001',
            '花露水': '130822220,1043058,122260004',
            '沐浴液': '130822220,1043058,1046966', '沐浴套装': '130822220,1043058,123650005',
            '泡澡用品': '130822220,1043058,122276003',
            '身体护理工具': '130822220,1043058,122706002', '身体护理套装': '130822220,1043058,1043503',
            '爽身粉': '130822220,1043058,1034756', '私处护理': '130822220,1043058,122282001',
            '脱毛膏': '130822220,1043058,1034769',
            '洗手液': '130822220,1043058,122282002', '香皂': '130822220,1043058,1046967', '浴盐': '130822220,1043058,1036814',
            '止汗香体': '130822220,1043058,1034760', '足部护理': '130822220,1043058,1046970',
            '足浴液': '130822220,1043058,122198008',
            '啫喱水': '130822220,10313,1043096', '宝宝护肤': '1501,122988005,122962009', '奶瓶清洗': '1501,122988005,122988008',
            '吸鼻器': '1501,122988005,123868001', '婴幼儿日常护理': '1501,122988005,1043789', '洗头帽': '1501,122988005,123864002',
            '婴儿理发器': '1501,122988005,122984007', '婴儿游泳池': '1501,122988005,123864001',
            '婴儿浴盆': '1501,122988005,123860003',
            '婴幼儿驱蚊防蚊': '1501,122988005,122992006', '婴幼儿洗衣液': '1501,122988005,122982008',
            '浴网': '1501,122988005,123862002'}


def date_time(delta):
    now = datetime.date.today()
    delta2 = datetime.timedelta(days=1)
    delta = datetime.timedelta(days=delta)
    n_days = now - delta2 - delta
    return (n_days.strftime('%Y-%m-%d'))

def spider_ali_index():
    f = open(r'.\proxy')
    lines = f.readlines()
    proxys = []
    page = 1
    #print(date_time(0))
    for i in range(0, len(lines)):
        ip = lines[i].strip("\n").split("\t")
        proxy_host = "http://" + ip[0] + ":" + ip[1]
        proxy_temp = {"http": proxy_host}
        proxys.append(proxy_temp)
    # 以上ip代理
    for i in range(len(searchList)):
        param = []
        id = dictList[searchList[i].strip()]
        # ws = w.add_sheet(str(searchList[i]),cell_overwrite_ok=True)
        url = 'https://index.1688.com/alizs/market.htm?userType=purchaser&cat=' + id
        print(url)
        time.sleep(1)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
        cookie = 'UM_distinctid=15acfcb25bd153-09d54b4190e9ba-34465264-100200-15acfcb25be2c9; cna=ynROEfc+dT0CAXTn9e3Agp46; _alizs_area_info_=1001; _alizs_user_type_=purchaser; JSESSIONID=kN78uOVG1-nANXLC0GeNQsXUZLT4-dlzmJFQ-3Bpy; alicnweb=touch_tb_at%3D1490858592100; ali_beacon_id=116.231.245.112.1490859382833.564009.0; _alizs_cate_info_=97%252C1042634%252C1042655; _tmp_ck_0=7YTzxwaBPWqPwwFMZ4Zr5EqrymZVhozWqpGsvNEcOeho2A0HUgtO56tnmBwpn5OlqH4RvT80ts6KZFRDA61j4FVSi7UjdvAXrLhrYgA%2FmIpZLEorFQnEGgIF0pZ%2BmYW%2Bv%2FWsx5nCF4g0PxVdonGv6%2FV6lQldqb7ctcv6KOnrVc67btAfq66iie3mU0CHkmryfVSKqw6wsXe6389sV7nRlOJZLD1bKwcdLIPhjPY5obfmzBCj0BnWgX5ogqLDQnLOT1vs0%2FUI67KbEH%2BOxPhrnPHZvCbLlcJhe0SjHFxlkl9KXibjZnStNiwLRRNz8qDNmxYFC1suzh%2BmtijDm908Q7zO%2BIXYeAoW2wl1QFrOs61l5MEOCdBQWw%3D%3D; l=AhgYtn-0M7ul7FrhvyfMnwF2aEyqAXyL; isg=AhISyYGRnnHPPOIZqm8bxA6fY9hucBa9krm3P9xrPkWw77LpxLNmzRgNKfyp'
        headers = {'User_Agent': user_agent, 'cookie': cookie}
        for proxy in proxys:
            try:
                # url=urllib.parse.quote(url)
                request = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(request)
                content = response.read()
                # print(content)
                soup = BeautifulSoup(content, "html.parser")
                values = soup.find(id='main-chart-val')["value"]
                dictvalues = simplejson.loads(values)
                # print(dictvalues)
                # print(type(values))
                # print(type(dictvalues))

                # print(time.strftime('%Y-%m-%d',time.localtime(time.time())))
                # pattern = re.compile("value='(.*?)'/>")
                # valuedic = re.findall(pattern,str(values))
                index_tb = dictvalues['purchaseIndexTb']['index']['history']
                indexcts_tb = dictvalues['purchaseIndexTb']['contrast']['history']
                index_1688 = dictvalues['purchaseIndex1688']['index']['history']
                indexcts_1688 = dictvalues['purchaseIndex1688']['contrast']['history']
                index_supply = dictvalues['supplyIndex']['index']['history']
                indexcts_supply = dictvalues['supplyIndex']['contrast']['history']
                # print(index_tb,indexcts_tb,index_1688,indexcts_1688,index_supply,indexcts_supply)

                for s in range(len(index_tb)):
                    param.append((searchList[i].strip(), date_time(s), index_tb[len(index_1688) - 1 - s],
                                  indexcts_tb[len(index_1688) - 1 - s], index_1688[len(index_1688) - 1 - s],
                                  indexcts_1688[len(index_1688) - 1 - s], index_supply[len(index_1688) - 1 - s],
                                  indexcts_supply[len(index_1688) - 1 - s]))
                print(param)
                # for i in range(len(param)):
                #     cursor.execute(sql.format(value=param[i]))
                #     db.commit()
                cursor.executemany(sql, param)
                db.commit()
                time.sleep(3)
                print('success')
                break
            except urllib.request.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
        page += 1
    cursor.close()
    db.close()


def ali2mysql():
    spider_ali_index()
    time.sleep(84600)
    return ali2mysql()


if __name__ == '__main__':
    ali2mysql()
