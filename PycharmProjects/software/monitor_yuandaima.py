#模块一：商品原始数据处理
# -*- encoding:utf-8 -*-
import re
import xlrd
from xlutils.copy import copy
import os
import  pandas as pd
import numpy as np

#获取指定路径下的文件名称
def get_filename(path):
    files = os.listdir(path)
    return files

# 读取原始数据，根据制定的处理规则清洗原始数据
def read_gz(filePath1, filePath2):#filePath1为待处理文件夹的路径，filePath2为存储已处理文件的路径
    filename = get_filename(filePath1)#获取路径下的文件名称
    for name in filename:
        data = xlrd.open_workbook(filename = filePath1 + name)
        #print(data.sheets())
        table = data.sheet_by_name('规则')
        nrows = table.nrows
        ncols = table.ncols

        if table.cell(1, 0).value == '天猫':
            tmget(filePath1, name, table.cell(1, 1).value, table.cell(1, 2).value)#按规则从天猫平台下原始数据提取有效数据
        elif table.cell(1, 0).value == '京东':
            jdget(filePath1, name, table.cell(1, 1).value, table.cell(1, 2).value)#按规则从京东平台下原始数据提取有效数据
        #    print(nrows)
        #    print(table.cell(0,0).value)
        if nrows > 2:
            for i in range(2, nrows):
                if '天猫' == table.cell(i, 0).value:
                    #print(table.cell(i, 0).value)
                    tmget(filePath2, name, table.cell(i, 1).value, table.cell(i, 2).value)
                elif '京东' == table.cell(i, 0).value:
                    #print(table.cell(i, 0).value)
                    jdget(filePath2, name, table.cell(i, 1).value, table.cell(i, 2).value)

# 根据制定的处理规则，提取天猫规则数据
def tmget(filePath2,name, zdname, keyname): #filePath2为文件路径，name为文件名，zdname为规则标题，keyname规则对应的关键字
    data = xlrd.open_workbook(filename=filePath2 + name)#打开工作薄
    table = data.sheet_by_name('天猫')#打开名为"天猫"的工作表
    nrows = table.nrows
    ncols = table.ncols
    # 复制一个用于写入的文件
    wb = copy(data)
    ws = wb.get_sheet(0)
    # 从原表格中获取其他信息写入新表格
    try:
        for i in range(1,nrows):
            for p in range(ncols):
                if str(table.cell(0, p).value) == str(zdname):
                    dprank = p

                if keyname + ':' in str(table.cell(i, p).value):

                    xinhao = table.cell(i, p).value.split(':')
                    if len(xinhao) > 1:
                        ws.write(i, dprank, xinhao[1])
        wb.save(filename)#保存提取的规则数据
    except Exception as e:
        print(e)
# 根据制定的处理规则，提取京东的规则数据
def jdget(filePath2, name, zdname, keyname):#filePath2为文件路径，name为文件名，zdname为规则标题，keyname规则对应的关键字
    data = xlrd.open_workbook(filename=filePath2+name)#打开工作薄
    table = data.sheet_by_name('京东')#打开名为"京东"的工作表
    nrows = table.nrows
    ncols = table.ncols
    # 复制一个用于写入的文件
    wb = copy(data)
    ws = wb.get_sheet(0)
    # print(table.cell(0,0).value)
    # 从原表格中获取其他信息写入新表格
    try:
        for i in range(1, nrows):
            for p in range(ncols):
                if table.cell(0, p).value == zdname:
                    dprank = p
                if keyname + '：' in  str(table.cell(i, p).value):
                    #print(table.cell(i,p).value)
                    xinhao = table.cell(i, p).value.split('：')
                    if len(xinhao) > 1:
                        ws.write(i, dprank, xinhao[1])
        wb.save(filename)#保存提取的规则数据
    except Exception as e:
        print(e)

#批量从提取完的规则数据中分离出目标数据
def extract_data(filePath):#filePath为规则数据的路径
    filename = get_filename(filePath)#获取规则数据的文件名称
    # 遍历分离出目标数据并保持
    for name in filename:
        #print(name)
        data = xlrd.open_workbook(filename= filePath+ name)
        writer = pd.ExcelWriter(filePath + name)
        writer1 = single_extract_data(data,writer)
        if os.path.isfile(filePath + name):
            os.remove(filePath + name)
        writer1.save()

#单个从提取完的规则数据中分离出目标数据
def single_extract_data(data,writer):#data为获取的工作薄对象
    table = data.sheets()[0]#获取第一个工作表对象
    nrows = table.nrows
    ncols = table.ncols
    xinhao1 = []
    #提取页字段名为“面网网址”前的所有数据列（包括“页面网址）并保存
    for p in range(ncols):
        if table.cell(0, p).value == '页面网址':
            dprank = p

    for i in range(1, nrows):

        chanping = {table.cell(0, dprank).value: table.cell(i, dprank).value.strip()}
        for j in range(dprank):
            chanping[table.cell(0, j).value] = str(table.cell(i, j).value).strip()

        xinhao1.append(chanping)

    df = pd.DataFrame(xinhao1)
    df.to_excel(writer, index = False, sheet_name = table.name)
    return writer

def main():
    word = ['天猫/', '京东/']
    for name in word:
        read_gz(filePath1 + name, filePath3 + name)
        extract_data(filePath3 + name)

if __name__ == '__main__':
    main()

#模块二：商品名称及字段处理
# -*- encoding:utf-8 -*-
import re
import xlrd
import os
import  pandas as pd
import numpy as np
#单个判断商品的链接是否为新链接，并将新旧链接分离
def judge_url_sx(df_old,df_new):#df_old为上一期商品的链接数据，df_new为当期商品的链接数据
    old_id = []#存储唯一标识上一期商品链接数据的列表
    new_id = []#存储唯一标识当期商品链接数据的列表
    df_same = pd.DataFrame(columns=df_new.columns)#存储当期旧链接的商品数据
    df_diff = pd.DataFrame(columns=df_new.columns)#存储当期新链接的商品数据
    for id in df_old.loc[:, '页面网址']:
        if re.search('.tmall' , id):
            nu = re.search('id=(\d+)', id)
            #print(nu.group(1))
            old_id.append(nu.group(1))
    for id in df_new.loc[:, '页面网址']:
        if re.search('.tmall', id):
            nu = re.search('id=(\d+)', id)
            # print(nu.group(1))
            new_id.append(nu.group(1))
    for url in range(len(df_new.loc[:, '页面网址'])):
        if re.search('.tmall' , df_new.loc[url, '页面网址']):
            if new_id[url] in old_id:
                df_same.loc[url] = df_new.loc[url]
            else:
                df_diff.loc[url] = df_new.loc[url]
        else:
            if str(df_new.loc[url, '页面网址']).strip() in df_old.loc[:,'页面网址'].values:

                df_same.loc[url] = df_new.loc[url]
            else:

                df_diff.loc[url] = df_new.loc[url]
    df_same = df_same.reset_index(drop=True)#以递增数字重排序dataframe的索引值
    df_diff = df_diff.reset_index(drop=True)#以递增数字重排序dataframe的索引值
    return (df_same, df_diff)

#批量判断商品的链接是否为新链接，并将新旧链接分离
def new_url_judge(fpath2,fpath3):#fpath2为上一期商品数据的路径，fpath3为当期商品数据的路径
    filename2 = get_filename(fpath3)#获取当前期商品数据的文件名
    print(filename2)
    #遍历当前期商品数据，将新旧链接数据分离并保存
    for name in filename2:
        df_old = pd.read_excel(fpath2 + name)
        df_new = pd.read_excel(fpath3 + name)
        df = pd.DataFrame(columns=df_new.columns)
        df = judge_url_sx(df_old, df_new)
        if os.path.isfile(fpath3 + name):
            os.remove(fpath3 + name)
        if os.path.isfile(fpath3 + name):
            os.remove(fpath3 + name)
        df[0].to_excel(fpath3 + name, index = False)
        df[1].to_excel(fpath3 + name, index=False)

#单个当期相同链接数据的名称及规格判断
def same_zd_judge(filePath,name):#filePath为当期商品数据的路径，name为商品数据的文件名称
    df_pool = pd.read_excel(filePath4 + name)#filePtah4为条件池的路径，获取商品数据在条件池中对应的池数据
    df = pd.read_excel(filePath + name)#获取当期的商品数据
    df['商品id'] = np.NaN#打池库商品id标签
    df['商品名称判断'] = np.NaN#打是否为商品名称判断出的标签
    df_title_same = pd.DataFrame(columns=df.columns)#存储名称规格都在池库的商品数据
    df_title_diff = pd.DataFrame(columns=df.columns)#存储名称或规格不在池库的商品数据
    guige1 = []#存储待判定数据的所有规格字段名
    [guige1.append(i) for i in df.columns if re.search('^规格', i)]
    #将待判定数据的规格单位进行标准转换
    for i in range(df.shape[0]):
        for j in range(df.loc[i,guige1].count()):
            if isinstance(df.loc[i,guige1[j]],str):
                df.loc[i,guige1[j]] = df.loc[i,guige1[j]].replace('M','m').replace('l','L').replace('K','k')
    guige2 = []#存储池库的所有规格字段名
    [guige2.append(i) for i in df_pool.columns if re.search('^规格', i)]
    keyword = []#存储池库所有关键字的字段名
    [keyword.append(i) for i in df_pool.columns if re.search('^关键字', i)]
    title = ['商品促销标题']#存储所有与商品名称相关的字段名称
    [title.append(i) for i in df.columns if re.search('^单品', i)]
    #对待判定数据进行名称及规格判断
    for i in range(df.shape[0]):
        name1 = False

        for p in range(df.loc[i, title].count()):
            print(df.loc[i,title[p]])
            for j in range(df_pool.shape[0]):

                for k in range(df_pool.loc[j, keyword].count()):

                    if isinstance(df_pool.loc[j, keyword[k]], str):
                        if df_pool.loc[j, keyword[k]] in str(df.loc[i, title[p]]):
                            name1 = True
                            if name1 == True:
                                name2 = False
                                df_pool_all = ''
                                for v in range(df_pool.loc[j, guige2].count()):
                                    df_pool_all += str(df_pool.loc[j, guige2[v]])
                                for u in range(len(guige1)):
                                    if isinstance(df.loc[i, guige1[u]], str):
                                        print(df.loc[i, guige1[u]])
                                        df.loc[i, guige1[u]] = df.loc[i, guige1[u]].replace(u'\xa0', u' ')

                                        for k in range(len(df.loc[i, guige1[u]].split(' '))):

                                            if df.loc[i, guige1[u]].split(' ')[k] not in df_pool_all:
                                                name2 = True
                                                df_title_diff.loc[i] = df.loc[i]
                                if name2 == False:
                                    df.loc[i, '商品id'] = df_pool.loc[j, '商品id']
                                    df_title_same.loc[i] = df.loc[i]

        if name1 == False:
            df.loc[i, '商品名称判断'] = '是'
            df_title_diff.loc[i] = df.loc[i]
    #print(df_title_same)
    #print(df_title_diff)
    return (df_title_same, df_title_diff)

#提取字符串中的数字、字母及右斜线“/”
def fun3_guige(s):
    if isinstance(s, str):
        s = s.replace('M', 'm').replace('l', 'L').replace('K', 'k').replace('G', 'g')
        s = ' '.join(set(re.findall('[.\da-zA-Z-/]*',s)))
    return s

#单个当期不同链接数据的名称及规格判断
def diff_zd_judge(filePath,name):#filePath为当期商品数据的路径，name为商品数据的文件名称
    df_pool = pd.read_excel(filePath4 + name)#filePtah4为条件池的路径，获取商品数据在条件池中对应的池数据
    df = pd.read_excel(filePath + name)#获取当期的商品数据
    df['商品id'] = np.NaN#打池库商品id标签
    df['商品名称判断'] = np.NaN#打是否为商品名称判断出的标签
    df_title_same = pd.DataFrame(columns=df.columns)#存储名称规格都在池库的商品数据
    df_title_diff = pd.DataFrame(columns=df.columns)#存储名称或规格不在池库的商品数据
    guige1 = []#存储待判定数据的所有规格字段名
    [guige1.append(i) for i in df.columns if re.search('^规格', i)]
    #将待判定数据的规格单位进行标准转换
    for i in range(df.shape[0]):
        for j in range(df.loc[i,guige1].count()):
            if isinstance(df.loc[i,guige1[j]],str):
                df.loc[i,guige1[j]] = df.loc[i,guige1[j]].replace('M','m').replace('l','L').replace('K','k')
    guige2 = []#存储池库的所有规格字段名
    [guige2.append(i) for i in df_pool.columns if re.search('^规格', i)]
    keyword = []#存储池库所有关键字的字段名
    [keyword.append(i) for i in df_pool.columns if re.search('^关键字', i)]
    title = ['商品促销标题']#存储所有与商品名称相关的字段名称
    [title.append(i) for i in df.columns if re.search('^单品', i)]
    #对待判定数据进行名称及规格判断
    for i in range(df.shape[0]):
        name1 = False

        for p in range(df.loc[i, title].count()):
            print(df.loc[i,title[p]])
            for j in range(df_pool.shape[0]):

                for k in range(df_pool.loc[j, keyword].count()):

                    if isinstance(df_pool.loc[j, keyword[k]], str):
                        if df_pool.loc[j, keyword[k]] in str(df.loc[i, title[p]]):
                            name1 = True
                            if name1 == True:
                                name2 = False
                                df_pool_all = ''
                                for v in range(df_pool.loc[j, guige2].count()):
                                    df_pool_all += str(df_pool.loc[j, guige2[v]])
                                for u in range(len(guige1)):
                                    if isinstance(df.loc[i, guige1[u]], str):
                                        print(df.loc[i, guige1[u]])
                                        df.loc[i, guige1[u]] = df.loc[i, guige1[u]].replace(u'\xa0', u' ')

                                        for k in range(len(df.loc[i, guige1[u]].split(' '))):

                                            if df.loc[i, guige1[u]].split(' ')[k] not in df_pool_all:
                                                name2 = True
                                                df_title_diff.loc[i] = df.loc[i]
                                if name2 == False:
                                    df.loc[i, '商品id'] = df_pool.loc[j, '商品id']
                                    df_title_same.loc[i] = df.loc[i]

        if name1 == False:
            df.loc[i, '商品名称判断'] = '是'
            df_title_diff.loc[i] = df.loc[i]
    #print(df_title_same)
    #print(df_title_diff)
    return (df_title_same, df_title_diff)

#批量当期相同链接数据的名称及规格判断
def same_url_zd_judge(filePath):#filePath为当期所有相同链接数据的路径
    filename = get_filename(filePath)#获取当期相同链接数据的所有文件名称
    #print(filename)
    #遍历所有相同链接的商品数据文件，进行名称及规格判定并保存
    for name in filename:
        df = same_zd_judge(filePath,name)
        if os.path.isfile(filePath + name):
            os.remove(filePath + name)
        if os.path.isfile(filePath + name):
            os.remove(filePath + name)
        df[0].to_excel(filePath + name,index=False)
        df[1].to_excel(filePath + name, index=False)

#批量当期不同链接数据的名称及规格判断
def diff_url_zd_judge(filePath):#filePath为当期所有不同链接数据的路径
    filename = get_filename(filePath)#获取当期不同链接数据的所有文件名称
    # print(filename)
    # 遍历所有不同链接的商品数据文件，进行名称及规格判定并保存
    for name in filename:
        df = diff_zd_judge(filePath, name)
        if os.path.isfile(filePath + name):
            os.remove(filePath + name)
        if os.path.isfile(filePath + name):
            os.remove(filePath + name)
        df[0].to_excel(filePath + name, index=False)
        df[1].to_excel(filePath + name, index=False)

#将当期商品数据加入到历史商品数据库
def url_pool(fpath1 , fpath2):#fpath1为历史商品数据库路径，fpath2为当期商品数据路径
    print(os.listdir(fpath2))
    #遍历当期商品数据的文件名称，将当期商品数据加入到历史数据库，去重并保存
    for path in os.listdir(fpath2):
        df1 =  pd.read_excel(fpath1 + path)#获取历史数据库
        print(len(df1))
        df2 = pd.read_excel(fpath2 + path)#获取当期数据
        df = pd.concat([df2,df1])#合并历史数据与当期数据
        df = df.reset_index(drop=True)#用数据字重排列dataframe的索引
        idd = []#创建列表存储唯一标识链接的id
        print(len(df))
        #去除合并后的重复商品数据，得到新的历史数据库并保存
        for i in range(len(df)):
            if re.search('tmall', df.loc[1, '页面网址']):
                if re.search('id=(\d+)', str(df.loc[i, '页面网址'])).group(1) in idd:
                    df.drop(i,inplace = True)
                else:
                    idd.append(re.search('id=(\d+)', str(df.loc[i, '页面网址'])).group(1))
            else:
                if df.loc[i,'页面网址'] in idd:
                    df.drop(i, inplace=True)
                else:
                    idd.append(df.loc[i,'页面网址'])
        if os.path.isfile(fpath2 + '提取数据1/'+ path):
            os.remove(fpath2 + '提取数据1/'+ path)
        print(len(df))
        print('---------------')
        df = df.reset_index(drop = True)
        df.to_excel(fpath2 + path , index = False)

def main():
    word = ['天猫/', '京东/']
    for name in word:
        new_url_judge(filePath2 + name, filePath3 + name)
        same_url_zd_judge(filePath3 + name)
        diff_url_zd_judge(filePath3 + name)
        url_pool(filePath2 + name,filePath3 + name)

if __name__ == '__main__':
    main()

#模块三：包装图片处理
# -*- encoding:utf-8 -*-
import os
import re
import logging
import pandas as pd
import  numpy as np
from PIL import Image
from collections import Counter

#获取图片R、G、B通道的像素值
def getrgb(image_file):#image_file为已读取的图片对象
    rs = []#存储R通道像素值
    gs = []#存储G通道像素值
    bs = []#存储B通道像素值
    for h in range(0, image_file.size[1]):  # h为图片的高度
        for w in range(0, image_file.size[0]):  # w为图片的宽度
            rs.append(image_file.getpixel((w, h))[0])
            gs.append(image_file.getpixel((w, h))[1])
            bs.append(image_file.getpixel((w, h))[2])
    # print  rs,gs,bs
    return rs, gs, bs

# 计算平均灰度值
def getAvg(ls):
    return sum(ls) / len(ls)

#计算单通道像素值的百分比，即相似度
def getMH(n, a, b):
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

#计算R、G、B各通道的像素平均值、找出R、G、B各通道像素值出现次数最多的元素
def getImgHash(fne):#fne为图片文件名
    image_file = Image.open(fne)  #获取图片的数据
    image_file = image_file.resize((35,35))#重置图片大小
    rgbls = getrgb(image_file)  #获取R、G、B3通道的像素值
    commonr = Counter(rgbls[0]).most_common(2)[0]#获取R通道数量最多的值
    commong = Counter(rgbls[1]).most_common(2)[0]#获取G通道数量最多的值
    commonb = Counter(rgbls[2]).most_common(2)[0]#获取B通道数量最多的值
    #print(commonr,commong,commonb)

    commonrgb = (commonr, commong, commonb)
    #去除R、G、B通道中数量最多的值对应的元素
    while commonr[0] in rgbls[0]:
        rgbls[0].remove(commonr[0])
    while commong[0] in rgbls[1]:
        rgbls[1].remove(commong[0])
    while commonb[0] in rgbls[2]:
        rgbls[2].remove(commonb[0])

    #计算R、G、B通道像素值的平均值
    avgr = getAvg(rgbls[0])  # R平均值
    avgg = getAvg(rgbls[1])  # G平均值
    avgb = getAvg(rgbls[2])  # B平均值
    avgrgb = (avgr, avgg, avgb)
    #print(avgrgb)
    return image_file, commonrgb, avgrgb

#将图片R、G、B各通道对应的像素值转为对应0、1、2的字符串
def main(image_file):
    file, commonrgb, avgrgb = getImgHash(image_file)

    rmark = getmark(file, 0, commonrgb, avgrgb)
    gmark = getmark(file, 1, commonrgb, avgrgb)
    bmark = getmark(file, 2, commonrgb, avgrgb)
    # print (rmark,gmark,bmark)
    return (rmark, gmark, bmark)

#将图片单通道对应的像素值转化为对应0、1、2的字符串
def getmark(file, n, commonrgb, avgrgb):
    rbitls = ''  # 接收获取0或1 除去变宽1px遍历像素
    for h in range(1, file.size[1] - 1):
        for w in range(1, file.size[0] - 1):
            #print(file.getpixel((w, h)))
            if file.getpixel((w, h))[n] == commonrgb[n][0]:
                rbitls = rbitls + '2'
            else:
                if file.getpixel((w, h))[n] >= avgrgb[n]:  # 像素的值比较平均值 大于记为1 小于记为0
                    rbitls = rbitls + '1'
                else:
                    rbitls = rbitls + '0'
    return rbitls, ]commonrgb[n][0, commonrgb[n][1]

#单文件包装图片判断，分离包装图片相同的商品数据
def pic_judge(name1,name2):#name1为上一期商品数据文件名，name2为当前期商品数据文件名
    df1 = pd.read_excel(name1)#获取上一期商品数据
    df2 = pd.read_excel(name2)#获取当期商品数据
    df_same = pd.DataFrame(columns=df2.columns)#存储包装图片相同的商品数据
    df_diff = pd.DataFrame(columns=df2.columns)#存储包装图片不同的商品数据
    df_same['图片链接_old'] = np.NaN
    df_diff['图片链接_old'] = np.NaN
    df_same['页面网址_old'] = np.NaN
    df_diff['页面网址_old'] = np.NaN
    df_same['相似度'] = np.NaN
    df_diff['相似度'] = np.NaN
    #print(df2)
    #遍历当期及上一期商品数据，进行包装图片判断，并分离出相同及不同包装图片的商品
    for i in range(df2.shape[0]):
        if re.search('.tmall',df2.loc[1,'页面网址']):
            url = re.search('id=(\d+)',df2.loc[i,'页面网址']).group(1)
            for j in range(df1.shape[0]):
                if url in df1.loc[j,'页面网址']:
                    pic1 = main(filename1)#filename1为文件名
                    pic2 = main(filename2)#filename2为文件名
                    comparer = getMH(0, pic1, pic2)
                    compareg = getMH(1,  pic1, pic2)
                    compareb = getMH(2,  pic1, pic2)
                    #print(comparer, compareg, compareb)
                    if comparer > 93 and compareg > 93 and compareb > 93:
                        #print(files[i], files[j], u'相似度', str(comparer) + '%', str(compareg) + '%', str(compareb) + '%')
                        df_same.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_same.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_same.loc[i, '相似度'] = (comparer + compareg + compareb)/3 #计算R、G、B通道的平均相似度
                        df_same.loc[i, df2.columns] = df2.loc[i]
                    else:
                        df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_diff.loc[i, '相似度'] = (comparer + compareg + compareb) / 3 #计算R、G、B通道的平均相似度
                        df_diff.loc[i, df2.columns] = df2.loc[i]
        else:
            for j in range(df1.shape[0]):
                if df1.loc[j,'页面网址'] == df2.loc[i,'页面网址']:
                    pic1 = main(filename1)#filename1为文件名
                    pic2 = main(filename2)#filename2为文件名
                    comparer = getMH(0, pic1, pic2)
                    compareg = getMH(1, pic1, pic2)
                    compareb = getMH(2, pic1, pic2)
                    # print(comparer, compareg, compareb)
                    if comparer > 93 and compareg > 93 and compareb > 93:
                        # print(files[i], files[j], u'相似度', str(comparer) + '%', str(compareg) + '%', str(compareb) + '%')
                        df_same.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_same.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_same.loc[i, '相似度'] = (comparer + compareg + compareb) / 3 #计算R、G、B通道的平均相似度
                        df_same.loc[i, df2.columns] = df2.loc[i]
                    else:
                        df_diff.loc[i, '图片链接_old'] = df1.loc[j, '图片链接']
                        df_diff.loc[i, '页面网址_old'] = df1.loc[j, '页面网址']
                        df_diff.loc[i, '相似度'] = (comparer + compareg + compareb) / 3 #计算R、G、B通道的平均相似度
                        df_diff.loc[i, df2.columns] = df2.loc[i]
    return (df_same , df_diff)

#批量文件包装图片判断，分离包装图片相同的商品数据并保存
def judge_pic(path2, path3):#path2为上一期所有文件的路径，path3为当期所有文件的路径
    word = ['天猫/', '京东/']#遍历不同平台数据
    for i in range(2):
        for name in os.listdir(path3):
            df = pic_judge(path2 + word[i] + name, path3 + word[i]+ name)
            if os.path.isfile(path3 + word[i] + name):
                os.remove(path3 + word[i] + name)
            df[0].to_excel(path3 + word[i] + name, index=False)
            if os.path.isfile(path3 + word[i] + name):
                os.remove(path3 + word[i] + name)
            df[1].to_excel(path3 + word[i] + name, index=False)
            print(df)

#建立数据处理日志文档
def logger(name):
    """ 获取logger"""
    logger = logging.getLogger()
    if not logger.handlers:
        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        # 文件日志
        file_handler = logging.FileHandler(r'C:\Users\tange\PycharmProjects\product_monitor\pic_log/'+ name+ '.log')
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值
        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(logging.INFO)
    return logger

#获取文件夹下的文件路径及文件名
def get_urllist(path):
    # 替换指定的文件夹路径即可
    base = (path)
    list = os.listdir(base)
    urlList = []
    for i in list:
        url = base + i
        urlList.append(url)
    return urlList

#比较图片相邻像素值大小，构造图片编码
def getCode(img, size=(9, 8)):
    result = []
    img = img.resize(size).convert('L')
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
    return str(result)

#计算图片的汉明距离
def compCode(code1, code2):
    num = 0
    for index in range(0, len(code1)):
        if code1[index] != code2[index]:
            num += 1
    return num

#计算两张图片的汉明距离
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
    return compCode(code1, code2)

#将当期新链接商品的包装图片放入历史包装图片库
def pic_repetition(path):#path为当期新链接商品数据的路径
    for name1 in ['天猫/', '京东/']:
        for name in os.listdir(path + name1):
            log = logger(name)
            code_List = []
            urlList = get_urllist(path+ name1 +  name + '/')
            for a in urlList:
                im = Image.open(a)
                pic_code = getCode(im,size=(9, 8))
                if (pic_code in code_List):
                    os.remove(a)
                    log.info("重复：%s" % a)
                else:
                    code_List.append(pic_code)
                    # print(md5List)
            print("一共%s张照片" % len(pic_code))
            #对新的图片库得文件名进行重命名
            urlList1 = get_urllist(path + name1 + name + '/')
            srcdir = path + name1 + name + '/'
            index = 1
            for srcfile in urlList1:
                sufix = os.path.splitext(srcfile)[1]
                destfile = srcdir + "//(" + u"%d" % (index) + ')' + sufix
                srcfile = os.path.join(srcdir, srcfile)
                os.rename(srcfile, destfile)
                index += 1

#新链接包装图片处理，判断新链接包装图片是否在历史包装图片库中
def judge_new_url_pic(filepath1, filepath2 ,filepath3):#filepath1为历史包装图片库的路径，filepath2为新链接对应的包装图片的路径，filepath3为新链接商品数据的路径
    word = ['天猫/', '京东/']
    for name1 in word:
        for name2 in os.listdir(filepath3 + name1):
            df = pd.read_excel(filepath3 + name1 + name2)
            md5List = {}
            urlList = get_urllist(filepath1 + name1 + '/' + name2 +'/')
            for a in urlList:
                im = Image.open(a)
                md5List[getCode(im)] = a
            print(md5List)
            for i in range(len(df)):
                im1 = Image.open(filepath2 + df.loc[i,'图片链接'])
                md5 = getCode(im1)
                print(md5)
                if md5 in md5List:
                    print(md5List[md5],md5)
                    df.loc[i,'旧图片名称'] = md5List[md5]
            if os.path.isfile(filepath3 + name1 + name2):
                os.remove(filepath3 + name1 + name2)
            df.to_excel(filepath3 + name1 + name2 ,index=False)

def main():
    judge_pic(filepath2, filepath3)
    judge_new_url_pic(filepath1, filepath2, filepath3)
    pic_repetition(path)
if __name__ == '__main__':
    main()
