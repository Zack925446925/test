import requests
import json
import hashlib
import pandas as pd
import  os
import numpy as np
import time
from threading import Timer
def getdata(date):
    
    url = 'http://120.24.240.170:1280/resSkin/getSkinTestData.shtml'

    randomString = 'djgjsgpsflfghsdoiuroesjgdsg'
    endstr = "&@**#pfjyfrjwb@&$"
    #headers = {'content-type': "application/json"}
     

    # 待加密信息
    str =randomString+url+endstr

    # 创建md5对象
    hl = hashlib.md5()

    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))

    print('MD5加密前为 ：' + str)
    print('MD5加密后为 ：' + hl.hexdigest())
    sign = hl.hexdigest()
    body = {"randomString": randomString, "sign": sign,'addDateTime':date}
    #print type(body)
    #print type(json.dumps(body))
    # 这里有个细节，如果body需要json形式的话，需要做处理
    # 可以是data = json.dumps(body)
    response = requests.post(url, data = body)#, headers = headersjson.dumps(body)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    #response  = requests.post(url, json = body, headers = headers)
     
    # 返回信息
    # print (response.text)
    # # 返回响应头
    # print (response.status_code)
    res = response.text
    print(res)
    df = pd.DataFrame(json.loads(res)['info'])
    user = get_user()
    print(list(user.keys()))
    df['名单客户'] = np.nan
    for i in range(len(df)):
        #print(df.loc[i, 'telephone'])
        if df.loc[i,'telephone'].strip() in list(user.keys()):
            print(df.loc[i,'telephone'])
            df.loc[i,'名单客户'] = user[df.loc[i,'telephone']]
    col_name = {'addDateTime':'addDateTime/测试时间', 'age':'age/实际年龄',  'nursingStatus':"nursingStatus/0护理前，1护理后",
       'skinAge':"skinAge/皮肤年龄", 'skinElasticity':"skinElasticity/弹性", 'skinOil':'skinOil/油分(计算后)', 'skinOil2':"skinOil2/油分", 'skinPosition':"skinPosition/测试部位",
       'telephone':"telephone/电话" , 'waterContent':"waterContent/水分"}
    df = df.rename(columns=col_name)
    if os.path.isfile('./数据导出.xlsx'):
        os.remove('./数据导出.xlsx')
    df.to_excel('./数据导出.xlsx',index=False)
    print('数据提取成功')
    df['时间标签'] = np.nan
    for i in range(len(df)):
        if fun2(df.loc[i,'addDateTime/测试时间']) < fun2(date+' 11:00:00'):
            df['时间标签'] = '早上'
        elif fun2(date+' 11:00:00') <= fun2(df.loc[i,'addDateTime/测试时间']) <= fun2(date+' 14:00:00'):
            df['时间标签'] = '中午'
        elif fun2(date+' 17:00:00') <= fun2(df.loc[i,'addDateTime/测试时间']) < fun2(date+' 20:00:00'):
            df['时间标签'] = '傍晚'
        elif fun2(date+' 20:00:00') <= fun2(df.loc[i,'addDateTime/测试时间']):
            df['时间标签'] = '晚上'
        else:
            df['时间标签'] = '在14点-17点之间，不按时间测量'
    return df
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
            if fun8(t[0]) < fun8(day + ' 11:00:00'):
                times['11点前'] += 1
            elif fun8(day + ' 11:00:00') <= fun8(t[0]) < fun8(day + ' 14:00:00'):
                times['11:00-14:00'] += 1
            elif fun8(day + ' 17:00:00') <= fun8(t[0]) < fun8(day + ' 20:00:00'):
                times['17:00-20:00'] += 1
            elif fun8(day + ' 20:00:00') <= fun8(t[0]):
                times['20:00之后'] += 1
    label = {}
    for key in times:
        if key in ['11点前','20:00之后']:
            num = times[key]-2
            if num<0:
                label[key] = 2-times[key]
        else:
            num = times[key] - 1
            if num<0:
                label[key] = 1-times[key]
    return label

def fun8(t):
    return time.mktime(time.strptime(t,"%Y-%m-%d %H:%M:%S"))
def check_data(days):
    df = pd.read_excel('./数据导出.xlsx')
    df = df[(df['skinPosition/测试部位'] == '脸颊') | (df['skinPosition/测试部位'] == '颈部')]
    df['时间索引'] = pd.to_datetime(df['addDateTime/测试时间'])
    #df['addDateTime/测试时间'] = df['addDateTime/测试时间'].apply(fun2)
    df = df.set_index('时间索引')
    #days = set(df.index)
    df_check=pd.DataFrame(columns=['姓名','测试时间','检查测试次数/脸颊为左脸','检查测试值','问题部位'])
    df_check_question = pd.DataFrame(columns=df.columns)
    df_all_times = pd.DataFrame(columns=['姓名','缺少次数/标准次数（10点前2次，11点-14点1次，17点-20点1次，20点之后2次）'])
    df_all_times_question = pd.DataFrame(columns=df.columns)
    question_num_all = []
    all_times = []
    print(type(df.index))
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
                    all_times.append([name,label])
                    df_all_times_question = pd.concat([df_all_times_question,df_day_name],ignore_index=True)
                for num  in num_dic:
                    question_num = [name]
                    per_time = num_dic[num]
                    if len(per_time)>0:
                        #print(per_time )
                        if len(per_time) < 6:
                            question_num.append(per_time[0])
                            question_num.append(dict(df_day_name.loc[per_time]['skinPosition/测试部位'].value_counts()))
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
                                question_num.append(list(dff[dff['skinPosition/测试部位']=='脸颊']['waterContent/水分'].apply(fun5).values))
                                question_num.append('左脸')
                                df_check_question = pd.concat([df_check_question, dff],ignore_index=True)

                            elif fun4(youlian)>5:
                                question_num.append(per_time[0])
                                question_num.append('没问题')
                                question_num.append(list(dff[dff['skinPosition/测试部位'] == '颈部']['waterContent/水分'].apply(fun5).values))
                                question_num.append('右脸')
                                df_check_question = pd.concat([df_check_question, dff],ignore_index=True)
                    if len(question_num)==5:
                        question_num1.append(question_num)
                question_num_all.extend(question_num1)
    for i in range(len(question_num_all)):
        df_check.loc[i] = question_num_all[i]
    for i in range(len(all_times)):
        df_all_times.loc[i] = all_times[i]
    if os.path.isfile('./检查数据.xlsx'):
        os.remove('./检查数据.xlsx')
    print(df_check)
    workbook = pd.ExcelWriter('./检查数据.xlsx')
    df_check.to_excel(workbook,'问题数据',index=False)
    df_check_question.to_excel(workbook,'问题数据源数据',index=False)
    df_all_times.to_excel(workbook,'次数检查',index=False)
    df_all_times_question.to_excel(workbook,'次数检查-源数据',index=False)
    workbook.save()

def skin2mysql():
    pass
def get_days_data():
    date = pd.date_range('20180301', periods=39)
    df0 = pd.DataFrame(columns=['addDateTime/测试时间', 'age/实际年龄', "nursingStatus/0护理前，1护理后",
                                "skinAge/皮肤年龄", "skinElasticity/弹性", 'skinOil/油分(计算后)',
                                "skinOil2/油分", "skinPosition/测试部位",
                                "telephone/电话", "waterContent/水分"])
    for dt in date:
        df0 = pd.concat([df0, getdata(str(dt)[:10])],ignore_index=True)
    df0.to_excel('./数据导出_多日期.xlsx',index=False)
if __name__ == '__main__':
    get_days_data()
    # with open('./取数日期.txt','r') as f:
    #     getdata(f.readlines())
    # with open('./检查日期.txt','r') as f:
    #     check_data(f.readlines())
