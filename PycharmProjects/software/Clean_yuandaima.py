#模块一 清洗获取有效数据
# -*- encoding:utf-8 -*-
import pandas as pd
import os
import numpy as np

#获取指定路径下的文件名称
def get_filename(path):
    files = os.listdir(path)
    return files

#根据制定的清洗规则，单个文件从原始数据提取有效数据
def extract_data(name1, name2, name3, name4,name5,num):#name1为指定品类制定的清洗规则的路径+文件名，name2为指定品类在确定平台下的采集数据的路径+文件名，name3为平台名，name4为采集数据的文件名，name5指定品类的名称，num为清洗规则工作表的编号
    df_title = pd.read_excel(name1,sheetname= num)#获取制定的清洗规则数据
    df_sourse = pd.read_excel(name2,encoding = 'utf-8')#获取待清洗的采集数据
    title1 = []#创建保存不需要分割的列数据字段名的列表
    [title1.append(df_title.iloc[i, 0]) for i in range(df_title.iloc[:,0].count())]
    df_new = pd.DataFrame(columns=title1)#创造保存有效数据的dataframe
    #print(df_new.columns)
    #提取不需要分割的列数据
    for j in title1:
        for i in df_sourse.columns:
            if i == j:
                df_new[i] = df_sourse[i]
    df_new.loc[:, df_title.iloc[0, 1]] = df_title.iloc[1, 1]#添加品类的名称
    #提取需要分割的单元格数据
    for i in range(df_sourse.shape[0]):
        for j in range(len(title1),df_sourse.shape[1]):
            if isinstance(df_sourse.iloc[i,j], str):
                df_sourse.iloc[i, j] = df_sourse.iloc[i, j].replace(u'\xa0',' ')
                if '：' in df_sourse.iloc[i, j]:
                    cell = df_sourse.iloc[i, j].split('：')
                    if cell[0] not in title1:
                        df_new.loc[i, cell[0]] = cell[1]
                        # print(cell[1])
                    else:
                        if df_new.loc[i, cell[0]] != cell[1]:
                            df_new.loc[i, cell[0]] = df_new.loc[i, cell[0]] + ' ' + cell[1]
                            #print(cell[1])
                elif ':' in df_sourse.iloc[i, j]:
                    cell = df_sourse.iloc[i, j].split(':')
                    if cell[0] not in title1:
                        df_new.loc[i, cell[0]] = cell[1]
                        print(cell[1])
                    else:
                        if df_new.loc[i, cell[0]] != cell[1]:
                            df_new.loc[i, cell[0]] = df_new.loc[i, cell[0]] + ' ' + cell[1]
        #print(df_new.loc[i])
    df_new.to_excel(filepath2 + name5 + '/' + name3 + '/' + name4, index=False)
    return df_new

#根据制定的清洗规则，批量从原始数据提取有效数据
def data_process(filepath1):#filepath1为待清洗数据的文件夹路径
    for nm in os.listdir(filepath1):#获取待清洗的品类名称
        path1 = filepath1 + nm +'/'
        filename1 = get_filename(path1)#获取指定品类数据采集的平台名
        print(filename1)
        #遍历采集指定品类数据的平台，清洗在该平台下采集到的品类数据
        for name in filename1:
            if name == '淘宝':
                num = 0
                name3 = '淘宝'
                path2 = filepath1 + nm + '/' + name + '/'
                filename2 = get_filename(path2)#获取指定品类在确定平台下保存采集数据的文件名
                for name2 in filename2:
                    extract_data(path1 + '规则.xlsx',path2 + name2, name3, name2 ,nm,num)
            elif name == '京东':
                num = 1
                name3 = '京东'
                path2 = filepath1 + nm + '/' + name + '/'
                filename2 = get_filename(path2)#获取指定品类在确定平台下保存采集数据的文件名
                for name2 in filename2:
                    extract_data(path1 + '规则.xlsx', path2 + name2, name3, name2 ,nm,num)
            elif name == '天猫':
                num = 2
                name3 = '天猫'
                path2 = filepath1 + nm + '/' + name + '/'
                filename2 = get_filename(path2)#获取指定品类在确定平台下保存采集数据的文件名
                for name2 in filename2:
                    extract_data(path1 + '规则.xlsx', path2 + name2, name3, name2 ,nm,num)

#模块二 清洗获取入库数据
# -*- encoding:utf-8 -*-
import re
import pandas as pd
import os
from dateutil.parser import parse
import numpy as np

#根据制定的入库数据规则，单个提取规范化后的入库数据
def get_data(name, df_guize):#name为待清洗的有效数据的文件路径+文件名，df_guize为以获取的入库规则数据
    df_source = pd.read_excel(name)#获取待入库的有效数据
    df_source = df_source.fillna(',')#以','填充数据中的缺失值
    title = list(df_source.columns)#获取有效数据的列标题
    keyword = []#保存属性相同的列标题名称
    [keyword.append(i) for i in df_guize.columns if re.search('^待提取', i)]
    df_new = pd.DataFrame(columns=df_guize.iloc[:, 0])#创建保存规范化后的入库数据的dataframe
    # print(len(df_guize),len(df_source))
    # print(title)
    # print(keyword)
    #将属性相同的字段合并到一列
    for i in range(len(title)):
        for j in range(len(df_guize)):
            for k in range(df_guize.loc[j, keyword].count()):
                if title[i] == df_guize.loc[j, keyword[k]]:
                    if df_new[df_guize.iloc[j, 0]].count() == 0:
                        df_new[df_guize.iloc[j, 0]] = df_source[title[i]]
                    else:
                        print(df_new[df_guize.iloc[j, 0]], df_source[title[i]])
                        df_new[df_guize.iloc[j, 0]] = pd.Series(list(map(fun, (
                        df_new[df_guize.iloc[j, 0]].astype(str) + ',' + df_source[title[i]].astype(str)))))
    #将值为'.'或','的数据替换为NaN
    for i in range(df_new.shape[1]):
        df_new.iloc[:, i] = pd.Series(list(map(fun1, df_new.iloc[:, i])))
    return df_new

#删除字符串两侧的中文和英文逗号
def fun(s):
    if isinstance(s, str):
        s = s.strip(',').strip('，')
    return s

#将字符串中的','或'.'替换成 NaN
def fun1(s):
    if s in [',', '.']:
        s = np.nan
    return s

#将字符串时间转换为'%Y-%m-%d'的时间类型
def fun2_datetime(s):
    if isinstance(s, str):
        s = parse(s).strftime('%Y-%m-%d')
    return s

#匹配字符串中的数字、大小写字母及右斜线
def fun3_guige(s):
    if isinstance(s, str):
        s = s.replace('M', 'm').replace('l', 'L').replace('K', 'k').replace('G', 'g')
        s = ','.join(list(set(re.findall('[.\da-zA-Z-/]*', s))))
    return s

#用'20'补全没有以'20'开头的字符串
def fun4_sstime(s):
    if isinstance(s, str):
        s = s.strip()
        if not re.match('^20', s):
            s = '20' + s
    return s

#将数据采集的平台名称标准化
def fun5_pt(s):
    if isinstance(s, str):
        if '搜全球购' in s:
            s = '淘宝全球购'
        elif '搜淘宝' in s:
            s = '淘宝'
        elif '天猫Tmall' in s:
            s = '天猫Tmall'
        elif '天猫超市' in s:
            s = '天猫超市'
        elif '天猫美妆' in s:
            s = '天猫美妆'
        elif '天猫国际' in s:
            s = '天猫国际'
    return s

#用空格替换字符串中的中英文问号、换行符及u'\xa0'，并删除两侧空格
def fun6_bm(s):
    if isinstance(s, str):
        s = s.replace('?', ' ').replace(u'\xa0', ' ').replace('？', ' ').replace('\n', ' ').strip()
    return s

#删除字符串中间的多余空格，仅保留一个空格
def fun7_kongge(s):
    if isinstance(s, str):
        k = []
        s = s.split(' ')
        for i in s:
            if i:
                k.append(i)
        k = ' '.join(k)
    return k

#根据制定的入库数据规则，批量提取规范化后的入库数据
def get_final_data(name, keword):#name为品类的名称，keyword为用于剔除非该品类的数据
    df_guize = pd.read_excel(filepath1)#filepath1为入库数据规则的文件路径+文件名
    df = pd.DataFrame(columns=df_guize.iloc[:, 0])#创建保存入库数据的dataframe
    #将不同平台下的所有指定品类的数据合并到一个dataframe中
    for name1 in os.listdir(filepath3 + name):#filepath3为不同平台保存有效数据的文件夹路径
        for name2 in os.listdir(filepath3 + name + '/' + name1):
            df = pd.concat([df, get_data(filepath3 + name + '/' + name1 + '/' + name2, df_guize)])
    df = df.reset_index(drop=True)#以数字递增的方式重置dataframe的索引
    print(df.index)
    #剔除非指定品类的数据
    for i in range(len(df)):
        if (keword not in str(df.loc[i, '商品名'])) and (keword not in str(df.loc[i, '单品'])):
            df.drop(i, inplace=True)
    df = df.reset_index(drop=True)
    print(len(df.index))
    #规范化入库数据
    df['爬取时间'] = pd.Series(list(map(fun2_datetime, df['当前时间'])))
    df['规格1'] = pd.Series(list(map(fun3_guige, df['规格'])))
    df['上市时间'] = pd.Series(list(map(fun4_sstime, df['上市时间'])))
    df['规格1'] = pd.Series(list(map(fun, df['规格1'])))
    df['平台'] = pd.Series(list(map(fun5_pt, df['平台'])))
    df['规格'] = pd.Series(list(map(fun7_kongge, df['规格'])))
    df = df[
        ['品类', '规格1', '上市时间', '商品产地', '价格', '税费', '销量', '店铺', '店铺年限', '店铺类型', '品牌', '累计评价', '平台', '品牌类型', '商品名', '库存',
         '规格', '发货', '商品编号', '单品', '适用类型', '保质期', '功效',
         '颜色分类', '当前时间', '页面网址', '爬取时间']]
    for i in range(len(df.columns)):
        if i != '页面网址':
            df.iloc[:, i] = pd.Series(list(map(fun6_bm, df.iloc[:, i])))
    js = df.to_json(orient='records', force_ascii=False)#将dataframe转换为json数据
    #将入库数据保存到json文件
    with open(filepath3 + name + '.json', 'w', encoding='utf-8') as f:
        f.write(js)
    print('成功提取：%s' % name)


def main():
    data_process(filepath)
    get_final_data(name , keyword)
if __name__ == '__main__':
    main()

#模块三 标准化数据导入数据库
# !/usr/bin/env python
""" 
Add a single line of code to the insert_autos function that will insert the
automobile data into the 'autos' collection. The data variable that is
returned from the process_file function is a list of dictionaries, as in the
example in the previous video.
"""
import json


def load(file):
    with open(file) as json_file:
        data = json.load(json_file)
        print(len(data))
        return data


# def process_file(infile):

# load('sample.osm.json')

def insert_autos(infile, db):
    data = load(infile)
    # Add your code here. Insert the data in one command.
    for i in range(len(data)):
        db.autos.insert(data[i])


if __name__ == "__main__":
    # Code here is for local use on your own computer.
    from pymongo import MongoClient

    client = MongoClient(URI)
    db = client.osmfinal

    insert_autos('file.json', db)
    # print db.autos.find_one()