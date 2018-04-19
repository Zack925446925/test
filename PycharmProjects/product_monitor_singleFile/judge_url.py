# -*- encoding:'utf-8' -*-
import pandas as pd
import numpy as np
import os
filepath1 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2017-10-25/提取数据/'
filepath2 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2017-11-1/提取数据/'
filepath3 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2017-11-1/链接判断/'
#获取文件名称
def get_filename(path):
    files = os.listdir(path)
    return files
#判断上新链接
def judge_url_sx(path1,path2,num,writer, name):
    df_old = pd.read_excel(path1+name, sheet_name=num)
    df_new = pd.read_excel(path2+name, sheet_name=num)
    df_new['判断是否为新增网址'] = np.NaN
    df_new['品牌名'] = name
    for url in range(len(df_new['页面网址'])):
        if df_new['页面网址'][url] in df_old['页面网址']:
            df_new['判断是否为新增网址'][url] = '否'
        else:
            df_new['判断是否为新增网址'][url] = '是'
    df = df_new[['品牌名','页面网址', '判断是否为新增网址']]
    df.to_excel(writer, index=False, sheet_name=str(num))
    writer.save()
#判断下架链接
def judge_url_xj(path1,path2,num,writer,name):
    df_old = pd.read_excel(path1, sheet_name=num)
    df_new = pd.read_excel(path2, sheet_name=num)
    df_old['判断是否为下线网址'] = np.NaN
    df_old['品牌名'] = name
    for url in range(len(df_old['页面网址'])):
        if df_old['页面网址'][url] in df_new['页面网址']:
            df_new['判断是否为下线网址'][url] = '否'
        else:
            df_new['判断是否为下线网址'][url] = '是'
    df = df_new[['品牌名','页面网址', '判断是否为新增网址']]
    df.to_excel(writer, index=False, sheet_name=str(num))
    writer.save()

def main():
    filename1 = get_filename(filepath1)
    filename2 = get_filename(filepath2)
    #print(filename1)
    #print(filename2)

    for name in filename2:
        if name in filename1:
            writer = pd.ExcelWriter(filepath3 + 'judge_url' + name)
            print(name)
            for i in range(2):
                judge_url_sx(filepath1, filepath2, i,writer,name)

if __name__ == '__main__':
    main()