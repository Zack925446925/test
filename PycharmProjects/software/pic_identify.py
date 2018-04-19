# -*- coding: utf-8 -*-
# 计算RGB各通道值，和均值比较，得出1,0,2，再比较
import pytesseract
from pytesser import *
from PIL import Image, ImageEnhance, ImageFilter
import os
import fnmatch
import re, time
from collections import Counter
import urllib, random


# import hashlib
def trygrt(image_file):
    try:
        getrgb(image_file)
        return True
    except Exception as e:
        return False


def getrgb(image_file):
    tmpls = []
    rs = []
    gs = []
    bs = []

    for h in range(0, image_file.size[1]):  # h
        for w in range(0, image_file.size[0]):  # w
            # print image_file,image_file.getpixel((w,h))
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
    if fenmu != 0:
        return dist * 100.0 / (fenmu)


def getImgHash(fne):
    image_file = Image.open(fne)  # 打开
    image_file = image_file.resize((15, 15))  # 重置图片大小我12px X 12px
    # image_file.save(fne+'.jpg')
    height, width = image_file.size

    # x = 4
    # y = 10
    # w = 8.5
    # h = 48
    # image_file = image_file.crop((x, y, x+w, y+h))

    image_fileg = image_file.convert("L")  # 转256灰度图
    image_file = image_fileg.convert("RGB")  # 转RGB图
    # image_file.show()
    rgbls = getrgb(image_file)  # rgb集合
    # commongray = Counter(Grayls).most_common(1)[0]
    commonr = Counter(rgbls[0]).most_common(2)[0]
    commong = Counter(rgbls[1]).most_common(2)[0]
    commonb = Counter(rgbls[2]).most_common(2)[0]
    # commonr2 = Counter(rgbls[0]).most_common(2)[1]
    # commong2 = Counter(rgbls[1]).most_common(2)[1]
    # commonb2 = Counter(rgbls[2]).most_common(2)[1]

    commonrgb = (commonr, commong, commonb)
    # print(commonrgb)
    # Grayls.remove(commongray[0])
    # avg=getAvg(Grayls)#灰度平均值
    # print rgbls[0]

    # print commonr[0]
    # print type(commonr[0])
    # print type(rgbls[0])
    # while commonr[0] in rgbls[0]:
    #    rgbls[0].remove(commonr[0])
    # while commong[0] in rgbls[1]:
    #    rgbls[1].remove(commong[0])
    # while commonb[0] in rgbls[2]:
    #    rgbls[2].remove(commonb[0])
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
            if file.getpixel((w, h))[n] == commonrgb[n][0]:
                rbitls = rbitls + '2'
            else:
                if file.getpixel((w, h))[n] >= avgrgb[n]:  # 像素的值比较平均值 大于记为1 小于记为0
                    rbitls = rbitls + '1'
                else:
                    rbitls = rbitls + '0'
    return rbitls, commonrgb[n][0], commonrgb[n][1]


# files1 = os.listdir(".//1")#图片文件夹地址自行替换
# files2 = os.listdir(".//2")#图片文件夹地址自行替换

# 从不同的excel文件中读取图片链接
toothlist = []
washlist = []
import xlrd
import codecs

data1 = xlrd.open_workbook(unicode('./牙膏/牙膏2017-12-29/天猫/天猫图片链接1.xlsx', "utf8"))  # 天猫图片/天猫图片链接.xlsx京东图片/京东详情链接.xlsx
table1 = data1.sheets()[0]  # 通过索引顺序获取
data2 = xlrd.open_workbook(unicode('./牙膏/牙膏2018-01-15/天猫/天猫图片链接1.xlsx', "utf8"))
table2 = data2.sheets()[0]  # 通过索引顺序获取
picurl1 = table1.col_values(3)
picurl2 = table2.col_values(3)
# print picurl2
result = codecs.open(r'result.txt', 'w', 'utf-8')


def picexist(n):
    try:
        Image.open(n)
        return True
    except Exception as e:
        # print e
        return False


print
len(picurl1), len(picurl2)
for i in range(1, len(picurl1)):
    # for j in range(i,len(picurl2)):
    if picexist(picurl1[i]) and picexist(picurl2[i]):
        a = main(picurl1[i])  # 图片地址自行替换
        # print (a)
        b = main(picurl2[i])
        comparer = getMH(0, a, b)
        compareg = getMH(1, a, b)
        compareb = getMH(2, a, b)
        if comparer < 100 and compareg < 100 and compareb < 100:  # and (comparer+compareg+compareb)/3>94
            print
            picurl1[i].encode('utf-8'), picurl2[i].encode('utf-8'), u'same', str(comparer) + '%', str(
                compareg) + '%', str(compareb) + '%'
            # print 'ff'
            # result.write((picurl1[i].encode('utf-8')+picurl2[i].encode('utf-8')+u'same'+str(comparer)+'%'+str(compareg)+'%'+str(compareb)+'%'))
    # else:
    #    print 'after pic miss',picurl1[i-1].encode('utf-8')
    if picexist(picurl1[i]):
        pass
    else:
        print
        'after pic miss', picurl1[i - 1].encode('utf-8')
    if picexist(picurl2[i]):
        pass
    else:
        print
        'after pic miss', picurl2[i - 1].encode('utf-8')
        # elif picexist(picurl1[i]):
        #     print 'after pic miss',picurl2[i-1].encode('utf-8')
        #    #result.write('after pic miss',picurl1[i-1].encode('utf-8'))
        # elif picexist (picurl2[i]):
        #    print 'after pic miss1',picurl1[i-1].encode('utf-8')
        #    #result.write('after pic miss1',picurl2[i-1].encode('utf-8'))
        # else:
        #    print 'after pic miss0',picurl2[i-1].encode('utf-8')
        # print main(".//yulanyou//1.jpg")[