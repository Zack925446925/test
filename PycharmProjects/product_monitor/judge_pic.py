
import cv2
import numpy as np
import pandas as pd
import os
import re

#同一品牌的两期图片链接数据判断，以图片链接为判断标准，分新上线和已下架



#获取文件名称
def get_filename(path):
    files = os.listdir(path)
    return files

#产品包装判断
def pic_sx_judge(filepath1,filepath2,name):
    df1 =  pd.read_excel(filepath1+name)
    df2 =  pd.read_excel(filepath2+name)
    df_same = pd.DataFrame(columns=df2.columns)
    df_diff = pd.DataFrame(columns=df2.columns)
    df_same['图片链接_old'] = np.NaN
    df_diff['图片链接_old'] = np.NaN
    df_same['页面网址_old'] = np.NaN
    df_diff['页面网址_old'] = np.NaN
    os.chdir(filepath4)

    for i in range(len(df2)):
        if re.search('.tmall',df2.loc[1,'页面网址']):

            url = re.search('id=(\d+)',df2.loc[i,'页面网址']).group(1)
            pic1 = df2.loc[i, '图片链接']
            for j in range(len(df1)):
                if url in df1.loc[j, '页面网址']:
                    pic2 = df1.loc[j, '图片链接']
                    try:
                        image1 = cv2.imread(pic1)
                        image2 = cv2.imread(pic2)
                        difference = cv2.subtract(image1, image2)
                        result = not np.any(difference)  # if difference is all zeros it will return False
                        if result is True:
                            df_same.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                            df_same.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                            df_same.loc[i, df2.columns] = df2.loc[i]

                        else:
                            df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                            df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                            df_diff.loc[i, df2.columns] = df2.loc[i]
                    except:
                        df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_diff.loc[i, df2.columns] = df2.loc[i]
        else:
            url = df2.loc[i, '页面网址']
            pic1 = df2.loc[i, '图片链接']
            for j in range(len(df1)):
                if url in df1.loc[j, '页面网址']:
                    pic2 = df1.loc[j, '图片链接']
                    try:
                        image1 = cv2.imread(pic1)
                        image2 = cv2.imread(pic2)
                        difference = cv2.subtract(image1, image2)
                        result = not np.any(difference)  # if difference is all zeros it will return False
                        if result is True:
                            df_same.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                            df_same.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                            df_same.loc[i, df2.columns] = df2.loc[i]

                        else:
                            df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                            df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                            df_diff.loc[i, df2.columns] = df2.loc[i]
                    except:
                        df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_diff.loc[i, df2.columns] = df2.loc[i]
    return (df_same,df_diff)

#商品上新判断
def new_judge(filepath1,filepath2):
    word = ['天猫/', '京东/']
    #word = ['京东/']
    for nm  in word:
        filename2 = get_filename(filepath2 + nm + '提取数据1/')
        print(filename2)
        for name in filename2:
            path1 = filepath1 + nm + '提取数据1/'
            path2 = filepath2 + nm + '提取数据1/'
            df = pic_sx_judge(path1, path2,name)
            if os.path.isfile(filepath2 + nm + '图片判断' + '/' + '相同图片/'+ name):
                os.remove(filepath2 + nm + '图片判断' + '/' + '相同图片/'+ name)
            if os.path.isfile(filepath2 + nm + '图片判断' + '/' + '不同图片/'+ name):
                os.remove(filepath2 + nm + '图片判断' + '/' + '不同图片/'+ name)
            df[0].to_excel(filepath2 + nm + '图片判断' + '/' + '相同图片/'+ name, index=False)
            df[1].to_excel(filepath2 + nm + '图片判断' + '/' + '不同图片/'+ name, index=False)
'''def match_pic_url(name1,name2,name3,num1=0, num2=1):
    df_right1 = pd.read_excel(name1)
    df_right2 = pd.read_excel(name2)
    df1 = pd.read_excel(name3,sheetname=num1)
    df2 = pd.read_excel(name3, sheetname=num2)
    writer = pd.ExcelWriter(name3)
    old_id = []
new_id = []
[old_id.append(re.search('id=(\d+)',df_right1.loc[i,'链接']).group(1))for i in range(len(df_right1))]
[new_id.append(re.search('id=(\d+)', df1.loc[i, '页面网址']).group(1)) for i in range(len(df1))]
    for i in range(len(df1)):
        url_id = re.search('id=(\d+)',df_right1.loc[i,'链接']).group(1)
        for j in range(len(df_right1)):
            if url_id in df_right1.loc[j,'链接']:
                df1.loc[i,'图片链接'] = df_right1.loc[j,'图片链接']
    for i in range(len(df2)):
        for j in range(len(df_right2)):
            if df2.loc[i,'页面网址'] == df_right2.loc[j,'链接']:
                df2.loc[i,'图片链接'] = df_right2.loc[j,'图片链接']
    if os.path.isfile(name3):
        os.remove(name3)
    df1.to_excel(writer, index=False, sheet_name='天猫')
    df2.to_excel(writer,index=False,sheet_name = '京东')
    writer.save()'''
def match_pic_url_single(name1,name3,name):
    df_right = pd.read_excel(name1)
    df = pd.read_excel(name3)
    writer = pd.ExcelWriter(name3)
    if len(df_right)>0:
        if re.search('tmall', df.loc[0, '页面网址']):
            for i in range(len(df)):
                print(df.loc[i, '页面网址'])
                id = re.search('id=(\d+)', df.loc[i, '页面网址']).group(1)
                for j in range(len(df_right)):
                    if id in df_right.loc[j,'链接'] :
                        df.loc[i, '图片链接'] = df_right.loc[j, '图片链接']
                        #print(df_right.loc[j, '图片链接'])
        else:
            for i in range(len(df)):
                for j in range(len(df_right)):
                    if df.loc[i, '页面网址'] == df_right.loc[j, '链接']:
                        df.loc[i, '图片链接'] = df_right.loc[j, '图片链接']
                        #print(df_right.loc[j, '图片链接'])
        if os.path.isfile(name3):
            os.remove(name3)
        df.to_excel(writer, index=False, sheet_name=name)
        writer.save()
def match_data(date):
    word = ['天猫/', '京东/']
    #word = ['京东/']
    for name  in word:
        filename1 = get_filename(filepath2+name+'提取数据1/')
        for name1 in filename1:
            print(name1)
            match_pic_url_single(filepath4 + date + name + name1,filepath2+ name + '提取数据1/' + name1,name.split('/')[0])
            #match_pic_url_single(filepath4 + '1.30/' + name + name1, filepath2 + name + '提取数据1/' + name1, name.split('/')[0])


# filepath1 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2018-2-28/'
# filepath2 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2018-3-31/'
# filepath4 = r'E:\A_judge_pic\2017-11-15/'

filepath1 = r'G:\01复硕正态\08项目\04中华项目监测\02成品数据\旗舰店数据\2018-3-31/'
filepath2 = r'G:\01复硕正态\08项目\04中华项目监测\02成品数据\旗舰店数据\2018-4-13/'
filepath4 = r'G:\A_judge_pic\toothpaste/'
if __name__ == '__main__':
    match_data('4.13/')
    #new_judge(filepath1, filepath2)
