# -*- coding:utf-8 -*-
import requests
import json
import hashlib
import pandas as pd
import  os
import numpy as np
import time
import pymysql

def getdata(date):
    url = 'http://120.24.240.170:1280/resSkin/getSkinTestData.shtml'

    randomString = 'djgjsgpsflfghsdoiuroesjgdsg'
    endstr = "&@**#pfjyfrjwb@&$"
    # 待加密信息
    str = randomString + url + endstr
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    sign = hl.hexdigest()
    body = {"randomString": randomString, "sign": sign, 'addDateTime': date}
    # print type(body)
    # print type(json.dumps(body))
    # 这里有个细节，如果body需要json形式的话，需要做处理
    # 可以是data = json.dumps(body)
    response = requests.post(url, data=body)  # , headers = headersjson.dumps(body)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    # response  = requests.post(url, json = body, headers = headers)

    # 返回信息
    # print (response.text)
    # # 返回响应头
    # print (response.status_code)
    res = response.text
    #print(res)
    df = pd.DataFrame(json.loads(res)['info'])
    user = get_user()
    #print(list(user.keys()))
    df['名单客户'] = np.nan
    for i in range(len(df)):
        # print(df.loc[i, 'telephone'])
        if df.loc[i, 'telephone'].strip() in list(user.keys()):
            #print(df.loc[i, 'telephone'])
            df.loc[i, '名单客户'] = user[df.loc[i, 'telephone']]
    col_name = {'addDateTime': 'addDateTime/测试时间', 'age': 'age/实际年龄', 'nursingStatus': "nursingStatus/0护理前，1护理后",
                'skinAge': "skinAge/皮肤年龄", 'skinElasticity': "skinElasticity/弹性", 'skinOil': 'skinOil/油分(计算后)',
                'skinOil2': "skinOil2/油分", 'skinPosition': "skinPosition/测试部位",
                'telephone': "telephone/电话", 'waterContent': "waterContent/水分"}
    df = df.rename(columns=col_name)
    df['age/实际年龄'] = df['age/实际年龄'].astype('int')
    df["nursingStatus/0护理前，1护理后"] = df["nursingStatus/0护理前，1护理后"].astype('int')
    df["skinAge/皮肤年龄"] = df["skinAge/皮肤年龄"].astype('int')
    df["skinElasticity/弹性"] = df["skinElasticity/弹性"].astype('float')
    df['skinOil/油分(计算后)'] = df['skinOil/油分(计算后)'].astype('float')
    df["skinOil2/油分"] = df["skinOil2/油分"].astype('float')
    df["waterContent/水分"] = df["waterContent/水分"].astype('float')
    df['名单客户'] = df['名单客户'].apply(fun9)
    df['时间标签'] = np.nan
    for i in range(len(df)):
        if fun8(date+' 5:00:00')<=fun8(df.loc[i,'addDateTime/测试时间'])<fun8(date+' 11:00:00'):
            df.loc[i,'时间标签'] = '早上'
        elif fun8(date+' 11:00:00')<=fun8(df.loc[i,'addDateTime/测试时间'])<fun8(date+' 14:00:00'):
            df.loc[i,'时间标签'] = '中午'
        elif fun8(date+' 17:00:00')<=fun8(df.loc[i,'addDateTime/测试时间'])<fun8(date+' 20:00:00'):
            df.loc[i,'时间标签'] = '傍晚'
        elif fun8(date+' 20:00:00')<=fun8(df.loc[i,'addDateTime/测试时间']):
            df.loc[i,'时间标签'] = '晚上'
        else:
            df.loc[i,'时间标签'] = '非规定时间'
    df['时间标签'] = df['时间标签'].apply(fun9)
    df['addDateTime/测试时间'] = pd.to_datetime(df['addDateTime/测试时间'])
    print(df.shape)
    return  df

def fun9(s):
    if str(s) == 'nan':
        s=''
    return s

def skin2mysql():
    day = time.strftime("%Y-%m-%d", time.localtime())
    print(type(day))
    df = getdata(day)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    print(df.shape)
    print(df)

    #df_all = df_all
    db = pymysql.connect("localhost", "root", "qwer1234", "skin_database", charset="utf8")
    cursor = db.cursor()
    sql = """replace into skin(addDateTime测试时间, age实际年龄, birthDate, deviceNumber, nursingStatus0护理前，1护理后, skinAge皮肤年龄,
    skinElasticity弹性,skinOil油分计算后,skinOil2油分,skinPosition测试部位,telephone电话,userName,waterContent水分,名单客户,时间标签)
    values
    {value}"""
    sql1 = """replace into skin_check_celiangzhi(姓名,测试时间,检查测试次数_脸颊为左脸,检查测试值,问题部位)
    values
    {value}"""
    sql2 = """replace into skin_check_cishu(姓名,测试时间,缺少次数)
    values
    {value}"""
    #插入皮肤原始数据
    for i in range(len(df)):
        # judge = str(df.loc[i,'addDateTime/测试时间'])+ df.loc[i,'telephone/电话']
        # if judge not in df_all['telephone/电话'].values:
        #print(df.loc[i].values)
        cursor.execute(sql.format(value=tuple(df.loc[i].values)))
        db.commit()
            # df.loc[i, 'telephone/电话'] = judge
            # df_all = df_all.append(df.loc[i],ignore_index=True)
    
    #插入皮肤检查数据
    df_check = check_data([day],df)
    for i in range(len(df_check[0])):
        # judge = str(df_check[0].loc[i,'测试时间'])
        # if judge not in df_check_all['测试时间'].values:
        print(df_check[0].loc[i].values)
        cursor.execute(sql1.format(value=tuple(df_check[0].loc[i].values)))
        db.commit()
            # df_check[0].loc[i, '测试时间'] = judge
            # df_check_all = df_check_all.append(df_check[0].loc[i],ignore_index=True)
    
    #插入次数检查数据
    for i in range(len(df_check[1])):
        # judge = str(df_check[1].loc[i,'测试时间']) + df_check[1].loc[i,'姓名']
        # if judge not in df_times_all['测试时间'].values:
        print(df_check[1].loc[i].values)
        cursor.execute(sql2.format(value=tuple(df_check[1].loc[i].values)))
        db.commit()
            # df_check[1].loc[i, '测试时间'] = judge
            # df_times_all = df_times_all.append(df_check[1].loc[i],ignore_index=True)
    cursor.close()
    db.close()
    #print(df_all)
    time.sleep(10)
    return skin2mysql()
def get_user():
    df = pd.read_excel('./受试者信息登记表20180320.xlsx')
    user_dic = {}
    for i in range(len(df)):
        user_dic[str(df.loc[i,'电话号码'])] = str(df.loc[i,'受访者姓名'])
    return user_dic
def fun1(t):
    t = t.strftime('%x')
    return t
def fun2(t):
    t= time.mktime(time.strptime(t,"%Y-%m-%d %H:%M:%S"))
    return t
def fun3(l):
    num_lis = []
    for i in range(1,7):
        for j in range(1,len(l)):
            if abs(time.mktime(time.strptime(l[j],"%Y-%m-%d %H:%M:%S"))-time.mktime(time.strptime(l[0],"%Y-%m-%d %H:%M:%S"))) > 900:
                num_lis.append(l[:j])
                l = l[j:]
                break
    num_lis.append(l)
    num = list(range(1,len(num_lis)+1))
    num_dic = dict(zip(num,num_lis))
    return num_dic
def fun4(l):
    if len(l)>0:
        s1 = max(l)
        s2 = min(l)
        num_lis =s1 - s2
    else:
        num_lis=0
    return num_lis

def fun5(l):
    if l:
        l = ('%.3f' % l)
    return l
def fun6(num_list,day):
    times = dict(zip(['11点前', '11:00-14:00', '17:00-20:00', '20:00之后'], [0, 0, 0, 0]))
    for t in num_list.values():
        if len(t)>0:
            if fun8(day + ' 5:00:00')< fun8(t[0]) < fun8(day + ' 11:00:00'):
                times['11点前'] += 1
            elif fun8(day + ' 11:00:00') <= fun8(t[0]) < fun8(day + ' 14:00:00'):
                times['11:00-14:00'] += 1
            elif fun8(day + ' 17:00:00') <= fun8(t[0]) < fun8(day + ' 20:00:00'):
                times['17:00-20:00'] += 1
            elif fun8(day + ' 20:00:00') <= fun8(t[0]):
                times['20:00之后'] += 1
    label = {}
    for key in times:
        if key in ['10点前','20:00之后']:
            num = times[key]-2
            if num<0:
                label[key] = 2-times[key]
        else:
            num = times[key] - 1
            if num<0:
                label[key] = 1-times[key]
    return label
def fun7(s):
    return s.strftime("%Y-%m-%d %H:%M:%S")
def fun8(t):
    return time.mktime(time.strptime(t,"%Y-%m-%d %H:%M:%S"))
def fun10(s):
    if s:
        return str(s)
    else:
        return ''

def check_data(days,df):
    df = df[(df['skinPosition/测试部位'] == '脸颊') | (df['skinPosition/测试部位'] == '颈部')]
    df['addDateTime/测试时间'] = df['addDateTime/测试时间'].apply(fun7)
    df['时间索引'] = pd.to_datetime(df['addDateTime/测试时间'])
    #df['addDateTime/测试时间'] = df['addDateTime/测试时间'].apply(fun2)
    df = df.set_index('时间索引')
    #days = set(df.index)
    df_check=pd.DataFrame(columns=['姓名','测试时间','检查测试次数/脸颊为左脸','检查测试值','问题部位'])
    df_check_question = pd.DataFrame(columns=df.columns)
    df_all_times = pd.DataFrame(columns=['姓名', '测试时间','缺少次数/标准次数（10点前2次，11点-14点1次，17点-20点1次，20点之后2次）'])
    df_all_times_question = pd.DataFrame(columns=df.columns)
    question_num_all = []
    all_times = []
    #print(df)
    for day in days:
        #df_day = df[day.strftime("%Y-%m-%d")]
        df_day = df[day.strip()]
        names = list(set(df_day['名单客户']))
        #print(df_day)
        #print(names)
        for name in names:
            if isinstance(name,str):
                df_day_name = df_day[df_day['名单客户']==name]
                df_day_name['索引'] = df_day_name['addDateTime/测试时间']
                num_dic = fun3(df_day_name['addDateTime/测试时间'].values)
                df_day_name = df_day_name.set_index('索引')
                question_num1 = []
                label = fun6(num_dic,day)
                if len(label)>0:
                    all_times.append([name,day,str(label)])
                    df_all_times_question = pd.concat([df_all_times_question,df_day_name],ignore_index=True)
                for num  in num_dic:
                    question_num = [name]
                    per_time = num_dic[num]
                    if len(per_time)>0:
                        #print(per_time )
                        if len(per_time) < 6:
                            question_num.append(per_time[0])
                            question_num.append(str(dict(df_day_name.loc[per_time]['skinPosition/测试部位'].value_counts())))
                            question_num.append('没检查值波动')
                            question_num.append('没问题')
                            df_check_question = pd.concat([df_check_question,df_day_name.loc[per_time]],ignore_index=True)

                        else:
                            dff = df_day_name.loc[per_time]
                            zuolian = list(dff[dff['skinPosition/测试部位']=='脸颊']['waterContent/水分'].values)
                            youlian = list(dff[dff['skinPosition/测试部位'] == '颈部']['waterContent/水分'].values)
                            print(zuolian)
                            print(youlian)
                            if fun4(zuolian)>5:
                                question_num.append(per_time[0])
                                question_num.append('没问题')
                                question_num.append(str(list(dff[dff['skinPosition/测试部位']=='脸颊']['waterContent/水分'].apply(fun5).values)))
                                question_num.append('左脸')
                                df_check_question = pd.concat([df_check_question, dff],ignore_index=True)

                            elif fun4(youlian)>5:
                                question_num.append(per_time[0])
                                question_num.append('没问题')
                                question_num.append(str(list(dff[dff['skinPosition/测试部位'] == '颈部']['waterContent/水分'].apply(fun5).values)))
                                question_num.append('右脸')
                                df_check_question = pd.concat([df_check_question, dff],ignore_index=True)
                    if len(question_num)==5:
                        question_num1.append(question_num)
                question_num_all.extend(question_num1)
    for i in range(len(question_num_all)):
        df_check.loc[i] = question_num_all[i]
    for i in range(len(all_times)):
        df_all_times.loc[i] = all_times[i]
    print(df_check, df_all_times)
    df_check['测试时间'] = pd.to_datetime(df_check['测试时间'])
    df_check['检查测试值'] = df_check['检查测试值'].apply(fun10)
    #df_all_times['测试时间'] = pd.to_datetime(df_all_times['测试时间'])
    #df_all_times['缺少次数/标准次数（10点前2次，11点-14点1次，17点-20点1次，20点之后2次）'] = df_all_times['缺少次数/标准次数（10点前2次，11点-14点1次，17点-20点1次，20点之后2次）'].apply(fun10)
    return df_check, df_all_times


if __name__ == '__main__':
    df_all = pd.DataFrame(columns=['addDateTime/测试时间',  'age/实际年龄', "nursingStatus/0护理前，1护理后",
                 "skinAge/皮肤年龄", "skinElasticity/弹性", 'skinOil/油分(计算后)',
                "skinOil2/油分","skinPosition/测试部位",
                 "telephone/电话",  "waterContent/水分"])
    df_check_all = pd.DataFrame(columns=['a姓名,测试时间','检查测试次数/脸颊为左脸','检查测试值','问题部位'])
    df_check_all = pd.DataFrame(columns=['a姓名,测试时间','缺少次数/标准次数（10点前2次，11点-14点1次，17点-20点1次，20点之后2次）'])
    skin2mysql()