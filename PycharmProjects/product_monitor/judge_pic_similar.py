# coding=utf-8
# 计算RGB各通道值，和均值比较，得出1,0,2，再比较
import pytesseract
# from pytesser import *
from PIL import Image, ImageEnhance, ImageFilter
import os
import fnmatch
import re, time
from collections import Counter
import urllib, random
import pandas as pd
import numpy as np

# import hashlib

def getrgb(image_file):
    tmpls = []
    rs = []
    gs = []
    bs = []
    for h in range(0, image_file.size[1]):  # h
        for w in range(0, image_file.size[0]):  # w
            # tmpls.append( image_file.getpixel((w,h))  )
            rs.append(image_file.getpixel((w, h))[0])
            gs.append(image_file.getpixel((w, h))[1])
            bs.append(image_file.getpixel((w, h))[2])
    # print  rs,gs,bs
    return rs, gs, bs


def getAvg(ls):  # 获取平均灰度值
    return sum(ls) / len(ls)


def getMH(n, a, b):  # 比较100个字符有几个字符相同
    dist = 0;
    fenmu = 0;
    # print(len(a[0]))
    for i in range(0, len(a[n][0])):
        # print(a[0][i])
        if a[n][0][i] != '2' and b[n][0][i] != '2':
            fenmu += 1
            if a[n][0][i] == b[n][0][i]:
                dist = dist + 1
                # print(fenmu)
    # print(dist)
    return dist * 100.0 / (fenmu)


def getImgHash(fne):
    image_file = Image.open(fne)  # 打开
    '''x = 100
    y = 0
    w = 150
    h = 350
    image_file = image_file.crop((x, y, x + w, y + h))
    image_file = image_file.resize((15, 35))  # 重置图片大小我12px X 12px
    # image_fileg=image_file.convert("L")#转256灰度图'''
    image_file = image_file.resize((35,35))
    rgbls = getrgb(image_file)  # rgb集合
    #print(rgbls)
    # commongray = Counter(Grayls).most_common(1)[0]
    commonr = Counter(rgbls[0]).most_common(2)[0]
    commong = Counter(rgbls[1]).most_common(2)[0]
    commonb = Counter(rgbls[2]).most_common(2)[0]
    #print(commonr,commong,commonb)
    # commonr2 = Counter(rgbls[0]).most_common(2)[1]
    # commong2 = Counter(rgbls[1]).most_common(2)[1]
    # commonb2 = Counter(rgbls[2]).most_common(2)[1]

    commonrgb = (commonr, commong, commonb)
    #print(commonrgb)
    # print(commonrgb)
    # Grayls.remove(commongray[0])
    # avg=getAvg(Grayls)#灰度平均值
    # print rgbls[0]

    # print commonr[0]
    # print type(commonr[0])
    # print type(rgbls[0])
    while commonr[0] in rgbls[0]:
        rgbls[0].remove(commonr[0])
    while commong[0] in rgbls[1]:
        rgbls[1].remove(commong[0])
    while commonb[0] in rgbls[2]:
        rgbls[2].remove(commonb[0])
    # while commonr2[0] in rgbls[0]:
    #    rgbls[0].remove(commonr2[0])
    # while commong2[0] in rgbls[1]:
    #    rgbls[1].remove(commong2[0])
    # while commonb2[0] in rgbls[2]:
    #    rgbls[2].remove(commonb2[0])
    avgr = getAvg(rgbls[0])  # r平均值
    avgg = getAvg(rgbls[1])  # r平均值
    avgb = getAvg(rgbls[2])  # r平均值
    avgrgb = (avgr, avgg, avgb)
    #print(avgrgb)
    return image_file, commonrgb, avgrgb
    # print  bitls,commongray[0],commongray[1]
    # return bitls,commongray[0],commongray[1]


'''''          
   m2 = hashlib.md5()    
   m2.update(bitls) 
   print m2.hexdigest(),bitls 
   return m2.hexdigest() 
'''


def main(image_file):
    file, commonrgb, avgrgb = getImgHash(image_file)

    rmark = getmark(file, 0, commonrgb, avgrgb)
    gmark = getmark(file, 1, commonrgb, avgrgb)
    bmark = getmark(file, 2, commonrgb, avgrgb)
    # print (rmark,gmark,bmark)
    return (rmark, gmark, bmark)


def getmark(file, n, commonrgb, avgrgb):
    rbitls = ''  # 接收获取0或1 除去变宽1px遍历像素
    for h in range(1, file.size[1] - 1):  # h
        for w in range(1, file.size[0] - 1):  # w
            #print(file.getpixel((w, h)))
            if file.getpixel((w, h))[n] == commonrgb[n][0]:
                rbitls = rbitls + '2'
            else:
                if file.getpixel((w, h))[n] >= avgrgb[n]:  # 像素的值比较平均值 大于记为1 小于记为0
                    rbitls = rbitls + '1'
                else:
                    rbitls = rbitls + '0'
    return rbitls, commonrgb[n][0], commonrgb[n][1]


def pic_judge(name1,name2):
    df1 = pd.read_excel(name1)
    df2 = pd.read_excel(name2)
    df_same = pd.DataFrame(columns=df2.columns)
    df_diff = pd.DataFrame(columns=df2.columns)
    if len(df2) > 0:
        df_same['图片链接_old'] = np.NaN
        df_diff['图片链接_old'] = np.NaN
        df_same['页面网址_old'] = np.NaN
        df_diff['页面网址_old'] = np.NaN
        df_same['相似度'] = np.NaN
        df_diff['相似度'] = np.NaN
        #print(df2)
        for i in range(df2.shape[0]):
            if re.search('.tmall',df2.loc[0,'页面网址']):
                url = re.search('id=(\d+)',df2.loc[i,'页面网址']).group(1)
                for j in range(df1.shape[0]):
                    if url in df1.loc[j,'页面网址']:
                        pic1 = main(filepath1 + df2.loc[i, '图片链接'])
                        pic2 = main(filepath1 + df1.loc[j, '图片链接'])
                        comparer = getMH(0, pic1, pic2)
                        compareg = getMH(1,  pic1, pic2)
                        compareb = getMH(2,  pic1, pic2)
                        #print(comparer, compareg, compareb)
                        if comparer > 85 and compareg > 85 and compareb > 85:  # and (comparer+compareg+compareb)/3>94
                            #print(files[i], files[j], u'相似度', str(comparer) + '%', str(compareg) + '%', str(compareb) + '%')
                            df_same.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                            df_same.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                            df_same.loc[i, '相似度'] = (comparer + compareg + compareb)/3
                            df_same.loc[i, df2.columns] = df2.loc[i]
                        else:
                            df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                            df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                            df_diff.loc[i, '相似度'] = (comparer + compareg + compareb) / 3
                            df_diff.loc[i, df2.columns] = df2.loc[i]
            else:
                for j in range(df1.shape[0]):
                    if df1.loc[j,'页面网址'] == df2.loc[i,'页面网址']:
                        pic1 = main(filepath1 + df2.loc[i, '图片链接'])
                        pic2 = main(filepath1 + df1.loc[j, '图片链接'])
                        comparer = getMH(0, pic1, pic2)
                        compareg = getMH(1, pic1, pic2)
                        compareb = getMH(2, pic1, pic2)
                        # print(comparer, compareg, compareb)
                        if comparer > 85 and compareg > 85 and compareb > 85:  # and (comparer+compareg+compareb)/3>94
                            # print(files[i], files[j], u'相似度', str(comparer) + '%', str(compareg) + '%', str(compareb) + '%')
                            df_same.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                            df_same.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                            df_same.loc[i, '相似度'] = (comparer + compareg + compareb) / 3
                            df_same.loc[i, df2.columns] = df2.loc[i]
                        else:
                            df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                            df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                            df_diff.loc[i, '相似度'] = (comparer + compareg + compareb) / 3
                            df_diff.loc[i, df2.columns] = df2.loc[i]
    #df_same.to_excel(r'C:\Users\tange\Desktop\测试数据/same六神.xls', index=False)
    #df_diff.to_excel(r'C:\Users\tange\Desktop\测试数据/diff六神.xls', index=False)
    return (df_same , df_diff)

# filepath1 = r'E:\A_judge_pic\2017-11-15/'
# filepath2 = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\2018-2-28/'
# filepath3 = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\2018-3-31/'

filepath1 = r'G:\A_judge_pic\toothpaste/'
filepath2 = r'G:\01复硕正态\08项目\04中华项目监测\02成品数据\旗舰店数据\2018-3-31/'
filepath3 = r'G:\01复硕正态\08项目\04中华项目监测\02成品数据\旗舰店数据\2018-4-13/'

def judge_pic(path2, path3):
    word = ['天猫/', '京东/']
    #word = ['京东/']
    for i in range(2):
        for name in os.listdir(path2 + word[i] + '提取数据1/'):
            df = pic_judge(path2 + word[i] + '提取数据1/' + name, path3 + word[i] + '提取数据1/' + name)
            if os.path.isfile(path3 + word[i] + '图片判断/' + '相同图片/' + name):
                os.remove(path3 + word[i] + '图片判断/' + '相同图片/' + name)
            df[0].to_excel(path3 + word[i] + '图片判断/' + '相同图片/' + name, index=False)
            if os.path.isfile(path3 + word[i] + '图片判断/' + '不同图片/' + name):
                os.remove(path3 + word[i] + '图片判断/' + '不同图片/' + name)
            df[1].to_excel(path3 + word[i] + '图片判断/' + '不同图片/' + name, index=False)
            print(df)
if __name__ == '__main__':
    judge_pic(filepath2,filepath3)
    #pic_judge(r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\2017-12-15\京东\提取数据1/六神.xls', r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\2017-12-29\京东\提取数据1/六神.xls')