from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
import pandas as pd
import os
import re
import  numpy as np
# This module can classfy the image by dHash
#
# author MashiMaroLjc
# version 2016-2-16
#box=(80,100,260,300)
#roi=img.crop(box)
#获取文件名称
def get_filename(path):
    files = os.listdir(path)
    return files
def getCode(img, size):
    result = []
    # print("x==",size[0])
    # print("y==",size[1]-1)

    x_size = size[0] - 1  # width
    y_size = size[1]  # high
    for x in range(0, x_size):
        for y in range(0, y_size):
            now_value = img.getpixel((x, y))
            next_value = img.getpixel((x + 1, y))

            if next_value < now_value:
                result.append(1)
            else:
                result.append(0)

    return result


def compCode(code1, code2):
    num = 0
    for index in range(0, len(code1)):
        if code1[index] != code2[index]:
            num += 1
    return num


def classfiy_dHash(image1, image2, size=(9, 8)):
    ''' 'image1' and 'image2' is a Image Object.
    You can build it by 'Image.open(path)'.
    'Size' is parameter what the image will resize to it and then image will be compared to another image by the dHash.
    It's 9 * 8 when it default.
    The function will return the hamming code,less is correct.
    '''
    image1 = image1.resize(size).convert('L')
    code1 = getCode(image1, size)

    image2 = image2.resize(size).convert('L')
    code2 = getCode(image2, size)

    assert len(code1) == len(code2), "error"
    #print('hello')
    return compCode(code1, code2)

def pic_judge(name1,name2):
    df1 = pd.read_excel(name1)
    df2 = pd.read_excel(name2)
    df_same = pd.DataFrame(columns=df2.columns)
    df_diff = pd.DataFrame(columns=df2.columns)
    df_same['图片链接_old'] = np.NaN
    df_diff['图片链接_old'] = np.NaN
    df_same['页面网址_old'] = np.NaN
    df_diff['页面网址_old'] = np.NaN
    #print(df2)
    for i in range(df2.shape[0]):
        if re.search('.tmall',df2.loc[1,'页面网址']):
            url = re.search('id=(\d+)',df2.loc[i,'页面网址']).group(1)
            for j in range(df1.shape[0]):
                if url in df1.loc[j,'页面网址']:
                    pic1 = Image.open(r'E:\A_judge_pic\2017-11-15/' + df2.loc[i, '图片链接'])
                    pic2 = Image.open(r'E:\A_judge_pic\2017-11-15/' + df1.loc[j, '图片链接'])
                    num = classfiy_dHash(pic2, pic1, size=(9, 8))
                    #print('-------------------------------------------')
                    if num == 0:
                        df_same.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_same.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_same.loc[i, df2.columns] = df2.loc[i]
                    else:
                        df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_diff.loc[i, df2.columns] = df2.loc[i]
        else:
            for j in range(df1.shape[0]):
                if df1.loc[j,'页面网址'] == df2.loc[i,'页面网址']:
                    pic1 = Image.open(r'E:\A_judge_pic\2017-11-15/' + df2.loc[i, '图片链接'])
                    pic2 = Image.open(r'E:\A_judge_pic\2017-11-15/' + df1.loc[j,'图片链接'])
                    num = classfiy_dHash(pic2, pic1, size = (9,8))
                    #print('-------------------------------------------')
                    if num == 0 :
                        df_same.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_same.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_same.loc[i, df2.columns] = df2.loc[i]
                    else:
                        df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_diff.loc[i, df2.columns] = df2.loc[i]
    return (df_same,df_diff)

filepath2 = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\2017-12-29/'
filepath3 = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\2018-1-15/'
def judge_pic(path2,path3):
    #word = ['天猫/', '京东/']
    word = ['天猫/']
    for i in range(2):
        for name in os.listdir(path2 + word[i] + '提取数据1/'):
            df = pic_judge(path2 + word[i] + '提取数据1/' + name, path3 + word[i] + '提取数据1/' + name)
            if os.path.isfile(path3 + word[i] + '图片判断/' + '相同图片/' + name):
                os.remove(path3 + word[i] + '图片判断/' + '相同图片/' + name)
            df[0].to_excel(path3 + word[i] + '图片判断/' + '相同图片/' + name, index=False)
            if os.path.isfile(path3 + word[i] + '图片判断/' + '不同图片/' + name):
                os.remove(path3 + word[i] + '图片判断/' + '不同图片/' + name)
            df[1].to_excel(path3 + word[i] + '图片判断/' + '不同图片/' + name, index=False)

if __name__ == '__main__':
    judge_pic(filepath2,filepath3)