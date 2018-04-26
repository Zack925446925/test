from wx import Frame
import wx
import xlrd
from xlutils.copy import copy
import os
import pandas as pd
import numpy as np
import re
from PIL import Image
from collections import Counter
import hashlib

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self, None, -1, title="test",  size=(1000, 600))
        panel = wx.Panel(self,-1)
        self.button1 = wx.Button(panel,-1,'提取相关数据',pos=(100,20))
        self.Bind(wx.EVT_BUTTON,self.main1,self.button1)
        self.button1.SetDefault()

        self.button2 = wx.Button(panel,-1,'匹配链接数据',pos=(100,70))
        self.Bind(wx.EVT_BUTTON,self.match_data,self.button2)
        self.button2.SetDefault()

        self.button3 = wx.Button(panel, -1, '规格名称判别', pos=(100, 120))
        self.Bind(wx.EVT_BUTTON, self.main2, self.button3)
        self.button3.SetDefault()

        self.button4 = wx.Button(panel, -1, '图片判别', pos=(100, 170))
        self.Bind(wx.EVT_BUTTON, self.main4, self.button4)
        self.button4.SetDefault()

        self.button5 = wx.Button(panel, -1, '新链接图片判断', pos=(100, 220))
        self.Bind(wx.EVT_BUTTON, self.main5, self.button5)
        self.button5.SetDefault()

        self.button6 = wx.Button(panel, -1, '将当期数据放入库中', pos=(100, 270))
        self.Bind(wx.EVT_BUTTON, self.main6, self.button6)
        self.button6.SetDefault()

        self.button7 = wx.Button(panel, -1, '将当期图片放入库中', pos=(100, 320))
        self.Bind(wx.EVT_BUTTON, self.main7, self.button7)
        self.button7.SetDefault()

        self.filepath1 = r'E:/01复硕正态/08项目/01沐浴露监测/01测试数据/01旗舰店数据/2018-3-31旗舰店数据/'
        self.filepath2 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2018-2-28/'
        self.filepath3 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2018-3-31/'
        self.filepath4 = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据/'
        self.filepath5 = r'E:\A_judge_pic\2017-11-15/'
        self.date = '3.31/'#修改日期

        # self.filepath1 = r'E:/01复硕正态/08项目/04中华项目监测/01测试数据/01旗舰店数据/2018-3-31旗舰店数据/'
        # self.filepath2 = r'E:/01复硕正态/08项目/04中华项目监测/02成品数据/旗舰店数据/2018-2-28/'
        # self.filepath3 = r'E:/01复硕正态/08项目/04中华项目监测/02成品数据/旗舰店数据/2018-3-31/'
        # self.filepath4 = r'E:\01复硕正态\08项目\04中华项目监测\02成品数据\旗舰店数据/'
        # self.filepath5 = r'G:\A_judge_pic\toothpaste/'
        # self.date = '4.13/'

    def main7(self,e):
        self.pic_repetition1(self.filepath4+'新链接判断图库/')
        print('将当期图片放入库中完成')
    def main5(self,e):
        self.judge_new_url_pic(self.filepath4+'新链接判断图库/',self.filepath5,self.filepath3)
        print('新链接图片判断完成')
    def main6(self,e):
        word = ['天猫/', '京东/']
        for name in word:
            self.url_pool(self.filepath2 + name,self.filepath3 + name)
        print('将当期数据放入库中完成')
    def main2(self,e):
        word = ['天猫/', '京东/']
        # word = ['京东/']
        for name in word:
            self.new_url_judge(self.filepath2 + name, self.filepath3 + name)
            self.same_url_zd_judge(self.filepath3 + name)
            self.diff_url_zd_judge(self.filepath3 + name)
        print('规格名称判别完成')
    def main1(self,e):
        word = ['天猫/', '京东/']
        # word = ['京东/']
        for name in word:
            self.read_gz(self.filepath1 + name, self.filepath3 + name)
            self.extract_data(self.filepath3 + name)
        print('提取相关数据完成')
    def match_data(self,e):
        word = ['天猫/', '京东/']
        # word = ['京东/']
        for name in word:
            filename1 = self.get_filename(self.filepath3 + name + '提取数据1/')
            for name1 in filename1:
                print(name1)
                self.match_pic_url_single(self.filepath5 + self.date + name + name1, self.filepath3 + name + '提取数据1/' + name1,
                                     name.split('/')[0])
        print('匹配链接数据完成')
    def main4(self,e):
        self.judge_pic(self.filepath2,self.filepath3)
        print('图片判别完成')

    def pic_repetition1(self,path):
        for name1 in ['天猫/', '京东/']:
            for name in os.listdir(path + name1):

                # log = logger(name)
                code_List = []
                urlList = self.get_urllist(path + name1 + name + '/')
                for a in urlList:
                    im = Image.open(a)
                    pic_code = self.getCode(im, size=(9, 8))
                    if (pic_code in code_List):
                        os.remove(a)
                        # log.info("重复：%s" % a)
                    else:
                        code_List.append(pic_code)
                        # print(md5List)
                print("一共%s张照片" % len(code_List))
                urlList1 = self.get_urllist(path + name1 + name + '/')
                srcdir = path + name1 + name + '/'
                index = 1
                for srcfile in urlList1:
                    sufix = os.path.splitext(srcfile)[1]
                    destfile = srcdir + "//(" + u"%d" % (index) + ')' + sufix
                    srcfile = os.path.join(srcdir, srcfile)
                    os.rename(srcfile, destfile)
                    index += 1

    def get_urllist(self,path):
        # 替换指定的文件夹路径即可
        base = (path)
        list = os.listdir(base)
        urlList = []
        for i in list:
            url = base + i
            urlList.append(url)
        return urlList

    def getCode(self,img, size=(9, 8)):
        result = []
        # print("x==",size[0])
        # print("y==",size[1]-1)
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

    def judge_new_url_pic(self,filepath1, filepath2, filepath3):
        word = ['天猫/', '京东/']
        for name1 in word:
            for name2 in os.listdir(filepath1 + name1):
                df = pd.read_excel(filepath3 + name1 + '不同链接数据提取' + '/' + name2 + '.xls')
                md5List = {}
                urlList = self.get_urllist(filepath1 + name1 + '/' + name2 + '/')
                for a in urlList:
                    im = Image.open(a)
                    md5List[self.getCode(im)] = a
                print(md5List)
                # print(md5List)
                for i in range(len(df)):
                    im1 = Image.open(filepath2 + df.loc[i, '图片链接'])
                    md5 = self.getCode(im1)
                    print(md5)
                    if md5 in md5List:
                        print(md5List[md5], md5)
                        print('****************')
                        df.loc[i, '旧图片名称'] = md5List[md5]
                if os.path.isfile(filepath3 + name1 + '不同链接数据提取' + '/' + name2 + '.xls'):
                    os.remove(filepath3 + name1 + '不同链接数据提取' + '/' + name2 + '.xls')
                df.to_excel(filepath3 + name1 + '不同链接数据提取' + '/' + name2 + '.xls', index=False)


    def url_pool(self,fpath1, fpath2):
        print(os.listdir(fpath2 + '提取数据1/'))
        for path in os.listdir(fpath2 + '提取数据1/'):
            df1 = pd.read_excel(fpath1 + '提取数据1/' + path)
            print(len(df1))
            df2 = pd.read_excel(fpath2 + '提取数据1/' + path)
            df = pd.concat([df2, df1])
            # df = df.reset_index(drop=True)
            df = df.reset_index(drop=True)
            idd = []
            print(len(df))

            for i in range(len(df)):
                if re.search('tmall', df.loc[i, '页面网址']):
                    if re.search('id=(\d+)', str(df.loc[i, '页面网址'])).group(1) in idd:
                        df.drop(i, inplace=True)
                    else:
                        idd.append(re.search('id=(\d+)', str(df.loc[i, '页面网址'])).group(1))
                else:
                    if df.loc[i, '页面网址'] in idd:
                        df.drop(i, inplace=True)
                    else:
                        idd.append(df.loc[i, '页面网址'])
            if os.path.isfile(fpath2 + '提取数据1/' + path):
                os.remove(fpath2 + '提取数据1/' + path)
            print(len(df))
            print('---------------')
            df = df.reset_index(drop=True)
            df.to_excel(fpath2 + '提取数据1/' + path, index=False)

    def getrgb(self,image_file):
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

    def getAvg(self,ls):  # 获取平均灰度值
        return sum(ls) / len(ls)

    def getMH(self,n, a, b):  # 比较100个字符有几个字符相同
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

    def getImgHash(self,fne):
        image_file = Image.open(fne)  # 打开
        '''x = 100
        y = 0
        w = 150
        h = 350
        image_file = image_file.crop((x, y, x + w, y + h))
        image_file = image_file.resize((15, 35))  # 重置图片大小我12px X 12px
        # image_fileg=image_file.convert("L")#转256灰度图'''
        image_file = image_file.resize((35, 35))
        rgbls = self.getrgb(image_file)  # rgb集合
        # print(rgbls)
        # commongray = Counter(Grayls).most_common(1)[0]
        commonr = Counter(rgbls[0]).most_common(2)[0]
        commong = Counter(rgbls[1]).most_common(2)[0]
        commonb = Counter(rgbls[2]).most_common(2)[0]
        # print(commonr,commong,commonb)
        # commonr2 = Counter(rgbls[0]).most_common(2)[1]
        # commong2 = Counter(rgbls[1]).most_common(2)[1]
        # commonb2 = Counter(rgbls[2]).most_common(2)[1]

        commonrgb = (commonr, commong, commonb)
        # print(commonrgb)
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
        avgr = self.getAvg(rgbls[0])  # r平均值
        avgg = self.getAvg(rgbls[1])  # r平均值
        avgb = self.getAvg(rgbls[2])  # r平均值
        avgrgb = (avgr, avgg, avgb)
        # print(avgrgb)
        return image_file, commonrgb, avgrgb

    def main(self,image_file):
        file, commonrgb, avgrgb = self.getImgHash(image_file)

        rmark = self.getmark(file, 0, commonrgb, avgrgb)
        gmark = self.getmark(file, 1, commonrgb, avgrgb)
        bmark = self.getmark(file, 2, commonrgb, avgrgb)
        # print (rmark,gmark,bmark)
        return (rmark, gmark, bmark)

    def getmark(self,file, n, commonrgb, avgrgb):
        rbitls = ''  # 接收获取0或1 除去变宽1px遍历像素
        for h in range(1, file.size[1] - 1):  # h
            for w in range(1, file.size[0] - 1):  # w
                # print(file.getpixel((w, h)))
                if file.getpixel((w, h))[n] == commonrgb[n][0]:
                    rbitls = rbitls + '2'
                else:
                    if file.getpixel((w, h))[n] >= avgrgb[n]:  # 像素的值比较平均值 大于记为1 小于记为0
                        rbitls = rbitls + '1'
                    else:
                        rbitls = rbitls + '0'
        return rbitls, commonrgb[n][0], commonrgb[n][1]

    def pic_judge(self,name1, name2):
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
            # print(df2)
            for i in range(df2.shape[0]):
                if re.search('.tmall', df2.loc[0, '页面网址']):
                    url = re.search('id=(\d+)', df2.loc[i, '页面网址']).group(1)
                    for j in range(df1.shape[0]):
                        if url in df1.loc[j, '页面网址']:
                            pic1 = self.main(self.filepath5 + df2.loc[i, '图片链接'])
                            pic2 = self.main(self.filepath5 + df1.loc[j, '图片链接'])
                            comparer = self.getMH(0, pic1, pic2)
                            compareg = self.getMH(1, pic1, pic2)
                            compareb = self.getMH(2, pic1, pic2)
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
                else:
                    for j in range(df1.shape[0]):
                        if df1.loc[j, '页面网址'] == df2.loc[i, '页面网址']:
                            pic1 = self.main(self.filepath5 + df2.loc[i, '图片链接'])
                            pic2 = self.main(self.filepath5 + df1.loc[j, '图片链接'])
                            comparer = self.getMH(0, pic1, pic2)
                            compareg = self.getMH(1, pic1, pic2)
                            compareb = self.getMH(2, pic1, pic2)
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
        # df_same.to_excel(r'C:\Users\tange\Desktop\测试数据/same六神.xls', index=False)
        # df_diff.to_excel(r'C:\Users\tange\Desktop\测试数据/diff六神.xls', index=False)
        return (df_same, df_diff)
    def judge_pic(self,path2, path3):
        word = ['天猫/', '京东/']
        # word = ['京东/']
        for i in range(2):
            for name in os.listdir(path2 + word[i] + '提取数据1/'):
                df = self.pic_judge(path2 + word[i] + '提取数据1/' + name, path3 + word[i] + '提取数据1/' + name)
                if os.path.isfile(path3 + word[i] + '图片判断/' + '相同图片/' + name):
                    os.remove(path3 + word[i] + '图片判断/' + '相同图片/' + name)
                df[0].to_excel(path3 + word[i] + '图片判断/' + '相同图片/' + name, index=False)
                if os.path.isfile(path3 + word[i] + '图片判断/' + '不同图片/' + name):
                    os.remove(path3 + word[i] + '图片判断/' + '不同图片/' + name)
                df[1].to_excel(path3 + word[i] + '图片判断/' + '不同图片/' + name, index=False)

    def tmget(self,filePath2, name, zdname, keyname):  # filePath2为文件路径，name为文件名，zdname为"字段"的值，keyname为"对应关键字"的值
        data = xlrd.open_workbook(filename=filePath2 + name)  # 打开工作薄
        table = data.sheet_by_name('天猫')  # 打开名为"天猫"的工作表
        nrows = table.nrows
        ncols = table.ncols
        # 复制一个用于写入的文件
        wb = copy(data)
        ws = wb.get_sheet(0)
        # 从原表格中获取其他信息写入新表格
        try:
            for i in range(1, nrows):
                for p in range(ncols):
                    if str(table.cell(0, p).value) == str(zdname):
                        dprank = p

                    if keyname + ':' in str(table.cell(i, p).value):

                        xinhao = table.cell(i, p).value.split(':')
                        if len(xinhao) > 1:
                            ws.write(i, dprank, xinhao[1])
            wb.save(self.filepath3 + '天猫/元数据1/' + name)
            # wb.save(r'E:\01复硕正态\08项目\03男士面霜\02成品数据\第三版/天猫/元数据1/' + name)
        except Exception as e:
            print(e)

    def jdget(self,filePath2, name, zdname, keyname):
        data = xlrd.open_workbook(filename=filePath2 + name)
        table = data.sheet_by_name('京东')
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
                    # if table.cell(0,p) != '页面网址':
                    #    clean_messy_code(table.cell(i,p))
                    if table.cell(0, p).value == zdname:
                        dprank = p
                    if keyname + '：' in str(table.cell(i, p).value):
                        #                    print(table.cell(i,p).value)
                        xinhao = table.cell(i, p).value.split('：')
                        if len(xinhao) > 1:
                            ws.write(i, dprank, xinhao[1])
            wb.save(self.filepath3 + '京东/元数据1/' + name)
            # wb.save(r'E:\01复硕正态\08项目\03男士面霜\02成品数据\第三版/京东/元数据1/' + name)
        except Exception as e:
            print(e)

    def new_url_judge(self,fpath2, fpath3):
        filename2 = self.get_filename(fpath3 + '提取数据1/')
        print(filename2)
        for name in filename2:
            df_old = pd.read_excel(fpath2 + '提取数据1/' + name)
            df_new = pd.read_excel(fpath3 + '提取数据1/' + name)
            df = pd.DataFrame(columns=df_new.columns)
            df = self.judge_url_sx(df_old, df_new)
            if os.path.isfile(fpath3 + '相同链接数据提取/' + name):
                os.remove(fpath3 + '相同链接数据提取/' + name)
            if os.path.isfile(fpath3 + '不同链接数据提取/' + name):
                os.remove(fpath3 + '不同链接数据提取/' + name)
            df[0].to_excel(fpath3 + '相同链接数据提取/' + name, index=False)
            df[1].to_excel(fpath3 + '不同链接数据提取/' + name, index=False)

    def judge_url_sx(self,df_old, df_new):
        # df_old = pd.read_excel(path1 + name, sheet_name=num)
        # df_new = pd.read_excel(path2 + name, sheet_name=num)
        # df_new['判断是否为新增网址'] = np.NaN
        old_id = []
        new_id = []
        df_same = pd.DataFrame(columns=df_new.columns)
        df_diff = pd.DataFrame(columns=df_new.columns)
        # [old_id.append(re.search('id=(\d+)', id)).group(1) for id in df_old.loc[:, '页面网址']]
        # [new_id.append(re.search('id=(\d+)', id)).group(1) for id in df_new.loc[:, '页面网址']]
        for id in df_old.loc[:, '页面网址']:
            if re.search('.tmall', id):
                nu = re.search('id=(\d+)', id)
                # print(nu.group(1))
                old_id.append(nu.group(1))
        for id in df_new.loc[:, '页面网址']:
            if re.search('.tmall', id):
                nu = re.search('id=(\d+)', id)
                # print(nu.group(1))
                new_id.append(nu.group(1))
        for url in range(len(df_new.loc[:, '页面网址'])):
            if re.search('.tmall', df_new.loc[url, '页面网址']):
                if new_id[url] in old_id:
                    # df_new.loc[url, '判断是否为新增'] = '否'
                    df_same.loc[url] = df_new.loc[url]
                else:
                    # df_new.loc[url, '判断是否为新增'] = '是'
                    df_diff.loc[url] = df_new.loc[url]
            else:
                if str(df_new.loc[url, '页面网址']).strip() in df_old.loc[:, '页面网址'].values:
                    # df_new.loc[url, '判断是否为新增'] = '否'
                    df_same.loc[url] = df_new.loc[url]
                else:
                    # df_new.loc[url, '判断是否为新增'] = '是'
                    df_diff.loc[url] = df_new.loc[url]
        df_same = df_same.reset_index(drop=True)
        df_diff = df_diff.reset_index(drop=True)
        return (df_same, df_diff)

    def same_zd_judge(self, filePath , name):
        df_pool = pd.read_excel(self.filepath4 + '条件池1/' + name)
        df = pd.read_excel(filePath + '相同链接数据提取/' + name)
        df_title_same = pd.DataFrame(columns=df.columns)
        df_title_diff = pd.DataFrame(columns=df.columns)
        df['商品id'] = np.NaN
        df['商品名称判断'] = np.NaN
        df_title_same = pd.DataFrame(columns=df.columns)
        df_title_diff = pd.DataFrame(columns=df.columns)
        guige1 = []
        [guige1.append(i) for i in df.columns if re.search('^规格', i)]
        if '上架规格' in df.columns:
            df['上架规格'] = df['上架规格'].map(self.fun3_guige)
            guige1.append('上架规格')
        for i in range(df.shape[0]):
            for j in range(df.loc[i, guige1].count()):
                if isinstance(df.loc[i, guige1[j]], str):
                    df.loc[i, guige1[j]] = df.loc[i, guige1[j]].replace('M', 'm').replace('l', 'L').replace('K', 'k')
        guige2 = []
        [guige2.append(i) for i in df_pool.columns if re.search('^规格', i)]
        keyword = []
        [keyword.append(i) for i in df_pool.columns if re.search('^关键字', i)]
        title = ['商品促销标题']
        [title.append(i) for i in df.columns if re.search('^单品', i)]
        for i in range(df.shape[0]):
            name1 = False

            for p in range(df.loc[i, title].count()):
                print(df.loc[i, title[p]])
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
        # print(df_title_same)
        # print(df_title_diff)
        return (df_title_same, df_title_diff)

    def fun3_guige(self,s):
        if isinstance(s, str):
            s = s.replace('M', 'm').replace('l', 'L').replace('K', 'k').replace('G', 'g')
            s = ' '.join(set(re.findall('[.\da-zA-Z-/]*', s)))
    def diff_zd_judge(self,filePath, name):
        df_pool = pd.read_excel(self.filepath4 + '条件池1/' + name)
        df = pd.read_excel(filePath + '不同链接数据提取/' + name)
        df_title_same = pd.DataFrame(columns=df.columns)
        df_title_diff = pd.DataFrame(columns=df.columns)
        df['商品id'] = np.NaN
        df['商品名称判断'] = np.NaN
        df_title_same = pd.DataFrame(columns=df.columns)
        df_title_diff = pd.DataFrame(columns=df.columns)
        # print(df_title_same, df_titile_diff)
        # if len(df.columns) > 0:
        # print(name)
        guige1 = []
        [guige1.append(i) for i in df.columns if re.search('^规格', i)]
        if '上架规格' in df.columns:
            df['上架规格'] = df['上架规格'].map(self.fun3_guige)
            guige1.append('上架规格')
        # print(guige1)
        for i in range(df.shape[0]):
            for j in range(df.loc[i, guige1].count()):
                if isinstance(df.loc[i, guige1[j]], str):
                    df.loc[i, guige1[j]] = df.loc[i, guige1[j]].replace('M', 'm').replace('l', 'L').replace('K', 'k')
        guige2 = []

        [guige2.append(i) for i in df_pool.columns if re.search('^规格', i)]
        # print(guige2)
        keyword = []
        [keyword.append(i) for i in df_pool.columns if re.search('^关键字', i)]
        # print(keyword)
        title = ['商品促销标题']
        [title.append(i) for i in df.columns if re.search('^单品', i)]
        # print(title)
        for i in range(df.shape[0]):
            name1 = False

            for p in range(df.loc[i, title].count()):
                # print(df.loc[i,title[p]])
                for j in range(df_pool.shape[0]):

                    for k in range(df_pool.loc[j, keyword].count()):

                        if isinstance(df_pool.loc[j, keyword[k]], str):
                            if df_pool.loc[j, keyword[k]] in str(df.loc[i, title[p]]):
                                # print(df_pool.loc[j, keyword[k]])
                                name1 = True
                                if name1 == True:
                                    name2 = False
                                    # print(df.loc[i, title[p]])
                                    for u in range(len(guige1)):
                                        if isinstance(df.loc[i, guige1[u]], str):
                                            # print(df.loc[i, guige1[u]])
                                            df.loc[i, guige1[u]] = df.loc[i, guige1[u]].replace(u'\xa0', u' ')
                                            for k in range(len(df.loc[i, guige1[u]].split(' '))):
                                                # print(df.loc[i, guige1[u]].split(' '))
                                                df_pool_all = ''
                                                for v in range(df_pool.loc[j, guige2].count()):
                                                    df_pool_all += str(df_pool.loc[j, guige2[v]])

                                                # print(df.loc[i, guige1[u]].split(' ')[k])
                                                # print(df_pool_all)
                                                if df.loc[i, guige1[u]].split(' ')[k].strip() not in df_pool_all:
                                                    name2 = True
                                                    df_title_diff.loc[i] = df.loc[i]
                                    if name2 == False:
                                        df.loc[i, '商品id'] = df_pool.loc[j, '商品id']
                                        df_title_same.loc[i] = df.loc[i]

            if name1 == False:
                df.loc[i, '商品名称判断'] = '是'
                df_title_diff.loc[i] = df.loc[i]

                # print(len(df_title_diff),len(df_title_same))
        return (df_title_same, df_title_diff)
    def diff_url_zd_judge(self,filePath):
        filename = self.get_filename(filePath + '不同链接数据提取/')
        # print(filename)
        for name in filename:
            df = self.diff_zd_judge(filePath, name)
            if os.path.isfile(filePath + '不是新品diff_url/' + name):
                os.remove(filePath + '不是新品diff_url/' + name)
            if os.path.isfile(filePath + '需手动确认的新品diff_url/' + name):
                os.remove(filePath + '需手动确认的新品diff_url/' + name)
            df[0].to_excel(filePath + '不是新品diff_url/' + name, index=False)
            df[1].to_excel(filePath + '需手动确认的新品diff_url/' + name, index=False)

    def same_url_zd_judge(self,filePath):
        filename = self.get_filename(filePath + '相同链接数据提取/')
        # print(filename)
        for name in filename:
            df = self.same_zd_judge(filePath, name)
            '''if os.path.isfile(filePath + '不是新品/' + name):
                os.remove(filePath + '不是新品/' + name)
            if os.path.isfile(filePath + '需手动确认的新品/'+ name):
                os.remove(filePath + '需手动确认的新品/'+ name)'''
            df[0].to_excel(filePath + '不是新品/' + name, index=False)
            df[1].to_excel(filePath + '需手动确认的新品/' + name, index=False)

    def match_pic_url_single(self,name1, name3, name):
        df_right = pd.read_excel(name1)
        df = pd.read_excel(name3)
        writer = pd.ExcelWriter(name3)
        if len(df_right) > 0:
            if re.search('tmall', df.loc[0, '页面网址']):
                for i in range(len(df)):
                    print(df.loc[i, '页面网址'])
                    id = re.search('id=(\d+)', df.loc[i, '页面网址']).group(1)
                    for j in range(len(df_right)):
                        if id in df_right.loc[j, '链接']:
                            df.loc[i, '图片链接'] = df_right.loc[j, '图片链接']
                            # print(df_right.loc[j, '图片链接'])
            else:
                for i in range(len(df)):
                    for j in range(len(df_right)):
                        if df.loc[i, '页面网址'] == df_right.loc[j, '链接']:
                            df.loc[i, '图片链接'] = df_right.loc[j, '图片链接']
                            # print(df_right.loc[j, '图片链接'])
            if os.path.isfile(name3):
                os.remove(name3)
            df.to_excel(writer, index=False, sheet_name=name)
            writer.save()
    def someEventHandler(self, event):
        '''
        定义一些事件处理函数用于给控件Bind
        '''
        pass


    # 提取数据
    def extract_data(self,filePath):
        filename = self.get_filename(filePath + '元数据1/')
        for name in filename:
            # print(name)
            data = xlrd.open_workbook(filename=filePath + '元数据1/' + name)
            writer = pd.ExcelWriter(filePath + '提取数据1/' + name)
            writer1 = self.single_extract_data(name, data, writer)
            if os.path.isfile(filePath + '提取数据1/' + name):
                os.remove(filePath + '提取数据1/' + name)
            writer1.save()

    def single_extract_data(self,name, data, writer):
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        xinhao1 = []
        for p in range(ncols):
            if table.cell(0, p).value == '页面网址':
                dprank = p

        for i in range(1, nrows):

            chanping = {table.cell(0, dprank).value: table.cell(i, dprank).value.strip()}
            for j in range(dprank):
                chanping[table.cell(0, j).value] = str(table.cell(i, j).value).strip()

            xinhao1.append(chanping)

        df = pd.DataFrame(xinhao1)
        df.to_excel(writer, index=False, sheet_name=table.name)
        return writer

    # 获取文件夹下的文件名
    def get_filename(self,path):
        files = os.listdir(path)
        return files

    # 读取规则信息
    def read_gz(self,filePath1,filePath2):
        filename = self.get_filename(filePath1)
        for name in filename:
            data = xlrd.open_workbook(filename=filePath1 + name)
            # print(data.sheets())
            table = data.sheet_by_name('规则')
            nrows = table.nrows
            ncols = table.ncols

            if table.cell(1, 0).value == '天猫':
                self.tmget(filePath1, name, table.cell(1, 1).value, table.cell(1, 2).value)
            elif table.cell(1, 0).value == '京东':
                self.jdget(filePath1, name, table.cell(1, 1).value, table.cell(1, 2).value)
            # print(nrows)
            #    print(table.cell(0,0).value)
            if nrows > 2:
                for i in range(2, nrows):
                    if '天猫' == table.cell(i, 0).value:
                        # print(table.cell(i, 0).value)
                        self.tmget(filePath2 + '元数据1/', name, table.cell(i, 1).value, table.cell(i, 2).value)
                    elif '京东' == table.cell(i, 0).value:
                        # print(table.cell(i, 0).value)
                        self.jdget(filePath2 + '元数据1/', name, table.cell(i, 1).value, table.cell(i, 2).value)


if __name__ == "__main__":
    app = wx.App()  # 创建应用的对象
    myframe = MyFrame()  # 创建一个自定义出来的窗口
    myframe.Show()  # 这两句一定要在MainLoop开始之前就执行
    app.MainLoop()