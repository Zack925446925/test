import requests
import json
import hashlib
import pandas as pd
import os
import numpy as np
import time
from threading import Timer
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
    df['addDateTime/测试时间'] = pd.to_datetime(df['addDateTime/测试时间'])
    df['age/实际年龄'] = df['age/实际年龄'].astype('int')
    df["nursingStatus/0护理前，1护理后"] = df["nursingStatus/0护理前，1护理后"].astype('int')
    df["skinAge/皮肤年龄"] = df["skinAge/皮肤年龄"].astype('int')
    df["skinElasticity/弹性"] = df["skinElasticity/弹性"].astype('float')
    df['skinOil/油分(计算后)'] = df['skinOil/油分(计算后)'].astype('float')
    df["skinOil2/油分"] = df["skinOil2/油分"].astype('float')
    df["waterContent/水分"] = df["waterContent/水分"].astype('float')
    df['名单客户'] = df['名单客户'].apply(fun1)
    # for i in range(len(df)):

    print(df.shape)
    return  df
def fun1(s):
    if str(s) == 'nan':
        s=''
    # print(s)
    # print(type(s))
    return s
def get_user():
    df = pd.read_excel('./受试者信息登记表20180320.xlsx')
    user_dic = {}
    for i in range(len(df)):
        user_dic[str(df.loc[i,'电话号码'])] = str(df.loc[i,'受访者姓名'])
    return user_dic
def skin2mysql(df_all):
    df = getdata(time.strftime("%Y-%m-%d", time.localtime()))
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    #df_all = df_all
    db = pymysql.connect("localhost", "root", "qwer1234", "skin_database", charset="utf8")
    cursor = db.cursor()
    sql='''insert ignore into skin(addDateTime测试时间,age实际年龄,birthDate,deviceNumber,nursingStatus0护理前，1护理后,skinAge皮肤年龄
    ,skinElasticity弹性,skinOil油分计算后,skinOil2油分,skinPosition测试部位,telephone电话,userName,waterContent水分,名单客户)
    values
    {value}'''
    cursor = db.cursor()
    for i in range(len(df)):
        judge = str(df.loc[i,'addDateTime/测试时间'])+ df.loc[i,'telephone/电话']
        if judge not in df_all['telephone/电话'].values:
            print(df.loc[i].values)
            cursor.execute(sql.format(value=tuple(df.loc[i].values)))
            db.commit()
            df.loc[i, 'telephone/电话'] = judge
            df_all = df_all.append(df.loc[i],ignore_index=True)

    cursor.close()
    db.close()
    print(df_all)
    time.sleep(7200)
    return skin2mysql(df_all)
if __name__ == '__main__':
    df_all = pd.DataFrame(columns=['addDateTime/测试时间',  'age/实际年龄', "nursingStatus/0护理前，1护理后",
                 "skinAge/皮肤年龄", "skinElasticity/弹性", 'skinOil/油分(计算后)',
                "skinOil2/油分","skinPosition/测试部位",
                 "telephone/电话",  "waterContent/水分"])
    skin2mysql(df_all)

