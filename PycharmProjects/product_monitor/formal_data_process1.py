# -*- encoding:utf-8 -*-
import re
import pandas as pd
import os
from dateutil.parser import parse
import numpy as np
import datetime, time


# 提取规格数据

# 获取文件夹下的文件名
def get_filename(path):
    files = os.listdir(path)
    return files


# 读取规则信息
def extract_data(name1, name2, name3, name4, name5, num):
    df_title = pd.read_excel(name1, sheetname=num)
    df_sourse = pd.read_excel(name2, encoding='utf-8')
    df_sourse = df_sourse.fillna(',')
    title1 = []
    [title1.append(df_title.iloc[i, 0]) for i in range(df_title.iloc[:, 0].count())]
    '''title2 = []
    for j in range(2):
    for i in range(df_title.iloc[:,j].count()):
        title2.append(df_title.iloc[i, j])
    [title3.append(df_title.iloc[i, j]) for j in range(2) for i in range(df_title.iloc[:,j]).count()]'''
    df_new = pd.DataFrame(columns=title1)
    # print(df_new.columns)
    for j in title1:
        for i in df_sourse.columns:
            if i == j:
                df_new[i] = df_sourse[i]
    df_new.loc[:, df_title.iloc[0, 1]] = df_title.iloc[1, 1]
    for i in range(df_sourse.shape[0]):
        for j in range(len(title1), df_sourse.shape[1]):
            if isinstance(df_sourse.iloc[i, j], str):
                df_sourse.iloc[i, j] = df_sourse.iloc[i, j].replace(u'\xa0', ' ').replace(u'\u2795', ' ').replace(u'\ufeff', ' ').replace(u'\u3ce0', ' ')
                if '：' in df_sourse.iloc[i, j]:
                    cell = df_sourse.iloc[i, j].split('：')
                    if cell[0] not in title1:
                        df_new.loc[i, cell[0]] = cell[1]
                        print(cell[1])
                    else:
                        if cell[1] not in str(df_new.loc[i, cell[0]]):
                            df_new.loc[i, cell[0]] = str(df_new.loc[i, cell[0]]) + ',' + cell[1]
                elif ':' in df_sourse.iloc[i, j]:
                    cell = df_sourse.iloc[i, j].split(':')
                    if cell[0] not in title1:
                        df_new.loc[i, cell[0]] = cell[1]
                        print(cell[1])
                    else:
                        if cell[1] not in str(df_new.loc[i, cell[0]]):
                            df_new.loc[i, cell[0]] = str(df_new.loc[i, cell[0]]) + ',' + cell[1]
    for i in range(df_new.shape[1]):
        df_new.iloc[:, i] = pd.Series(list(map(fun, df_new.iloc[:, i])))
        df_new.iloc[:, i] = pd.Series(list(map(fun1, df_new.iloc[:, i])))
    df_new.to_excel(filepath2 + name5 + '/' + name3 + '/' + name4, index=False)
    return df_new

def data_process():
    for nm in os.listdir(filepath1):
        path1 = filepath1 + nm + '/'
        filename1 = get_filename(path1)
        print(filename1)
        for name in filename1:
            if name == '淘宝':
                num = 0
                name3 = '淘宝'
                path2 = filepath1 + nm + '/' + name + '/'
                filename2 = get_filename(path2)
                for name2 in filename2:
                    extract_data(path1 + '规则.xlsx', path2 + name2, name3, name2, nm, num)
            elif name == '京东':
                num = 1
                name3 = '京东'
                path2 = filepath1 + nm + '/' + name + '/'
                filename2 = get_filename(path2)
                for name2 in filename2:
                    extract_data(path1 + '规则.xlsx', path2 + name2, name3, name2, nm, num)
            elif name == '天猫':
                num = 2
                name3 = '天猫'
                path2 = filepath1 + nm + '/' + name + '/'
                filename2 = get_filename(path2)
                for name2 in filename2:
                    extract_data(path1 + '规则.xlsx', path2 + name2, name3, name2, nm, num)


def data_process1(nm):
    path1 = filepath1 + nm + '/'
    filename1 = get_filename(path1)
    print(filename1)
    for name in filename1:
        if name == '淘宝':
            num = 0
            name3 = '淘宝'
            path2 = filepath1 + nm + '/' + name + '/'
            filename2 = get_filename(path2)
            for name2 in filename2:
                extract_data(path1 + '规则.xls', path2 + name2, name3, name2, nm, num)
        elif name == '京东':
            num = 1
            name3 = '京东'
            path2 = filepath1 + nm + '/' + name + '/'
            filename2 = get_filename(path2)
            for name2 in filename2:
                extract_data(path1 + '规则.xls', path2 + name2, name3, name2, nm, num)
        elif name == '天猫':
            num = 2
            name3 = '天猫'
            path2 = filepath1 + nm + '/' + name + '/'
            filename2 = get_filename(path2)
            for name2 in filename2:
                extract_data(path1 + '规则.xls', path2 + name2, name3, name2, nm, num)


def get_data(name, df_guize):
    df_source = pd.read_excel(name)
    df_source = df_source.fillna(',')
    title = list(df_source.columns)
    keyword = []
    [keyword.append(i) for i in df_guize.columns if re.search('^待提取', i)]
    df_new = pd.DataFrame(columns=df_guize.iloc[:, 0])
    # print(len(df_guize),len(df_source))
    # print(title)
    # print(keyword)
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

    for i in range(df_new.shape[1]):
        df_new.iloc[:, i] = pd.Series(list(map(fun1, df_new.iloc[:, i])))
    return df_new


def fun(s):
    if isinstance(s, str):
        s = s.strip(',').strip('，')
    return s


def fun1(s):
    if s in [',', '.']:
        s = np.nan
    return s


def fun2_datetime(s):
    if isinstance(s, str):
        s = parse(s).strftime('%Y-%m-%d')
    return s


def fun3_guige(s):
    if isinstance(s, str):
        s = s.replace('M', 'm').replace('l', 'L').replace('K', 'k').replace('G', 'g')
        s = ','.join(list(set(re.findall('[.\da-zA-Z-/]*', s))))
    return s


def fun4_sstime(s):
    if isinstance(s, str):
        s = s.strip()
        if not re.match('^20', s):
            s = '20' + s
    return s


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


def fun6_bm(s):
    if isinstance(s, str):
        s = s.replace('?', ' ').replace(u'\xa0', ' ').replace('？', ' ').replace('\n', ' ').strip()
    return s


def fun7_kongge(s):
    k = []
    if isinstance(s, str):
        s = s.split(' ')
        for i in s:
            if i:
                k.append(i)
        k = ' '.join(k)

    return k

def fun8_fanxiexian(s):
    if isinstance(s,str):
        s = s.strip('\\')
    return s
def get_final_data(name, keword):
    df_guize = pd.read_excel(r'C:\Users\Administrator\Desktop\常规数据清洗\入库数据/数据库字段规则.xls')
    df = pd.DataFrame(columns=df_guize.iloc[:, 0])
    for name1 in os.listdir(filepath3 + name):
        for name2 in os.listdir(filepath3 + name + '/' + name1):
            df = pd.concat([df, get_data(filepath3 + name + '/' + name1 + '/' + name2, df_guize)])
    df = df.reset_index(drop=True)
    print(df.index)
    for i in range(len(df)):
        if (keword not in str(df.loc[i, '商品名'])) and (keword not in str(df.loc[i, '单品'])):
            df.drop(i, inplace=True)
    df = df.reset_index(drop=True)
    print(len(df.index))
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
            df.iloc[:, i] = pd.Series(list(map(fun8_fanxiexian, df.iloc[:, i])))
    '''if os.path.isfile(filepath3 + '入库数据' + '/' + name + '.csv'):
        os.remove(filepath3 + '入库数据' + '/' + name + '.csv')
    df.to_csv(filepath3 + '入库数据' + '/' + name + '.csv',index = False)'''
    # df.to_excel(filepath3 + '入库数据' + '/' + name + '.xlsx',index = False)
    s = df.to_json(orient='records', force_ascii=False)
    with open(filepath3 + '入库数据' + '/' + name + '.json', 'w', encoding='ANSI') as f:
        f.write(s)
    print('成功提取：%s' % name)


filepath1 = r'E:\01复硕正态\07数据清洗\02测试数据\2018-2-1/'
filepath2 = r'E:\01复硕正态\07数据清洗\01成品数据\2018-2-1/'
filepath3 = r'C:\Users\Administrator\Desktop\常规数据清洗\入库数据\2018-1-18/'


def main():
    # get_final_data('面部按摩霜','按摩')
    data_process1('peeling')
    #get_final_data('男士防晒', '防晒')

    '''for name in os.listdir(filepath3):
        get_final_data(name)'''


if __name__ == '__main__':
    main()



