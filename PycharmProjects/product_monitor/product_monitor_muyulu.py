# -*- encoding:utf-8 -*-
import re
import xlwt
import xlrd
from xlutils.copy import copy
import os
import  pandas as pd
import numpy as np

#获取文件夹下的文件名
def get_filename(path):
    files = os.listdir(path)
    return files

# 读取规则信息
def read_gz(filePath1, filePath2):
    filename = get_filename(filePath1)
    for name in filename:
        data = xlrd.open_workbook(filename = filePath1 + name)
        #print(data.sheets())
        table = data.sheet_by_name('规则')
        nrows = table.nrows
        ncols = table.ncols

        if table.cell(1, 0).value == '天猫':
            tmget(filePath1, name, table.cell(1, 1).value, table.cell(1, 2).value)
        elif table.cell(1, 0).value == '京东':
            jdget(filePath1, name, table.cell(1, 1).value, table.cell(1, 2).value)
        #    print(nrows)
        #    print(table.cell(0,0).value)
        if nrows > 2:
            for i in range(2, nrows):
                if '天猫' == table.cell(i, 0).value:
                    #print(table.cell(i, 0).value)
                    tmget(filePath2 + '元数据1/', name, table.cell(i, 1).value, table.cell(i, 2).value)
                elif '京东' == table.cell(i, 0).value:
                    #print(table.cell(i, 0).value)
                    jdget(filePath2 + '元数据1/', name, table.cell(i, 1).value, table.cell(i, 2).value)

# 提取天猫规则数据
def tmget(filePath2,name, zdname, keyname): #filePath2为文件路径，name为文件名，zdname为"字段"的值，keyname为"对应关键字"的值
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
        wb.save(filePath3+'天猫/元数据1/' + name)
        #wb.save(r'E:\01复硕正态\08项目\03男士面霜\02成品数据\第三版/天猫/元数据1/' + name)
    except Exception as e:
        print(e)
#提取京东规则数据
def jdget(filePath2, name, zdname, keyname):
    data = xlrd.open_workbook(filename=filePath2+name)
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
                #if table.cell(0,p) != '页面网址':
                #    clean_messy_code(table.cell(i,p))
                if table.cell(0, p).value == zdname:
                    dprank = p
                if keyname + '：' in  str(table.cell(i, p).value):
                    #                    print(table.cell(i,p).value)
                    xinhao = table.cell(i, p).value.split('：')
                    if len(xinhao) > 1:
                        ws.write(i, dprank, xinhao[1])
        wb.save(filePath3+'京东/元数据1/' + name)
        #wb.save(r'E:\01复硕正态\08项目\03男士面霜\02成品数据\第三版/京东/元数据1/' + name)
    except Exception as e:
        print(e)

#提取数据
def extract_data(filePath):
    filename = get_filename(filePath+ '元数据1/')
    for name in filename:
        #print(name)
        data = xlrd.open_workbook(filename= filePath+ '元数据1/' + name)
        writer = pd.ExcelWriter(filePath+ '提取数据1/'  + name)
        writer1 = single_extract_data(name,data,writer)
        if os.path.isfile(filePath+ '提取数据1/'  + name):
            os.remove(filePath+ '提取数据1/'  + name)
        writer1.save()

def single_extract_data(name,data,writer):
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
    df.to_excel(writer, index = False, sheet_name = table.name)
    return writer

def judge_url_sx(df_old,df_new):
    #df_old = pd.read_excel(path1 + name, sheet_name=num)
   # df_new = pd.read_excel(path2 + name, sheet_name=num)
    #df_new['判断是否为新增网址'] = np.NaN
    old_id = []
    new_id = []
    df_same = pd.DataFrame(columns=df_new.columns)
    df_diff = pd.DataFrame(columns=df_new.columns)
    #[old_id.append(re.search('id=(\d+)', id)).group(1) for id in df_old.loc[:, '页面网址']]
    #[new_id.append(re.search('id=(\d+)', id)).group(1) for id in df_new.loc[:, '页面网址']]
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
                #df_new.loc[url, '判断是否为新增'] = '否'
                df_same.loc[url] = df_new.loc[url]
            else:
                #df_new.loc[url, '判断是否为新增'] = '是'
                df_diff.loc[url] = df_new.loc[url]
        else:
            if str(df_new.loc[url, '页面网址']).strip() in df_old.loc[:,'页面网址'].values:
                #df_new.loc[url, '判断是否为新增'] = '否'
                df_same.loc[url] = df_new.loc[url]
            else:
                #df_new.loc[url, '判断是否为新增'] = '是'
                df_diff.loc[url] = df_new.loc[url]
    df_same = df_same.reset_index(drop=True)
    df_diff = df_diff.reset_index(drop=True)
    return (df_same, df_diff)

def new_url_judge(fpath2,fpath3):
    filename2 = get_filename(fpath3 + '提取数据1/')
    print(filename2)
    for name in filename2:
        df_old = pd.read_excel(fpath2 + '提取数据1/'+ name)
        df_new = pd.read_excel(fpath3 + '提取数据1/'+ name)
        df = pd.DataFrame(columns=df_new.columns)
        df = judge_url_sx(df_old, df_new)
        if os.path.isfile(fpath3 + '相同链接数据提取/' + name):
            os.remove(fpath3 + '相同链接数据提取/' + name)
        if os.path.isfile(fpath3 + '不同链接数据提取/' + name):
            os.remove(fpath3 + '不同链接数据提取/' + name)
        df[0].to_excel(fpath3 + '相同链接数据提取/' + name, index = False)
        df[1].to_excel(fpath3 + '不同链接数据提取/' + name, index=False)

#名称规格判断
def same_zd_judge(filePath,name):
    df_pool = pd.read_excel(filePath4+'条件池1/'+name)
    df = pd.read_excel(filePath + '相同链接数据提取/' + name)
    df_title_same = pd.DataFrame(columns=df.columns)
    df_title_diff = pd.DataFrame(columns=df.columns)
    df['商品id'] = np.NaN
    df['商品名称判断'] = np.NaN
    df_title_same = pd.DataFrame(columns=df.columns)
    df_title_diff = pd.DataFrame(columns=df.columns)
    guige1 = []
    [guige1.append(i) for i in df.columns if re.search('^规格', i)]
    for i in range(df.shape[0]):
        for j in range(df.loc[i,guige1].count()):
            if isinstance(df.loc[i,guige1[j]],str):
                df.loc[i,guige1[j]] = df.loc[i,guige1[j]].replace('M','m').replace('l','L').replace('K','k')
    guige2 = []
    [guige2.append(i) for i in df_pool.columns if re.search('^规格', i)]
    keyword = []
    [keyword.append(i) for i in df_pool.columns if re.search('^关键字', i)]
    title = ['商品促销标题']
    [title.append(i) for i in df.columns if re.search('^单品', i)]
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


def fun3_guige(s):
    if isinstance(s, str):
        s = s.replace('M', 'm').replace('l', 'L').replace('K', 'k').replace('G', 'g')
        s = ' '.join(set(re.findall('[.\da-zA-Z-/]*',s)))
    return s
#名称规格判断
def diff_zd_judge(filePath,name):
    df_pool = pd.read_excel(filePath4+'条件池1/'+name)
    df = pd.read_excel(filePath + '不同链接数据提取/' + name)
    df_title_same = pd.DataFrame(columns=df.columns)
    df_title_diff = pd.DataFrame(columns=df.columns)
    df['商品id'] = np.NaN
    df['商品名称判断'] = np.NaN
    df_title_same = pd.DataFrame(columns=df.columns)
    df_title_diff = pd.DataFrame(columns=df.columns)
    #print(df_title_same, df_titile_diff)
    #if len(df.columns) > 0:
    #print(name)
    guige1 = []
    [guige1.append(i) for i in df.columns if re.search('^规格', i)]
    if '上架规格' in df.columns:
        df['上架规格'] = df['上架规格'].map(fun3_guige)
        guige1.append('上架规格')
    #print(guige1)
    for i in range(df.shape[0]):
        for j in range(df.loc[i,guige1].count()):
            if isinstance(df.loc[i,guige1[j]],str):
                df.loc[i,guige1[j]] = df.loc[i,guige1[j]].replace('M','m').replace('l','L').replace('K','k')
    guige2 = []

    [guige2.append(i) for i in df_pool.columns if re.search('^规格', i)]
    #print(guige2)
    keyword = []
    [keyword.append(i) for i in df_pool.columns if re.search('^关键字', i)]
    #print(keyword)
    title = ['商品促销标题']
    [title.append(i) for i in df.columns if re.search('^单品', i)]
    #print(title)
    for i in range(df.shape[0]):
        name1 = False

        for p in range(df.loc[i, title].count()):
            #print(df.loc[i,title[p]])
            for j in range(df_pool.shape[0]):

                for k in range(df_pool.loc[j, keyword].count()):

                    if isinstance(df_pool.loc[j, keyword[k]], str):
                        if df_pool.loc[j, keyword[k]] in str(df.loc[i, title[p]]):
                            #print(df_pool.loc[j, keyword[k]])
                            name1 = True
                            if name1 == True:
                                name2 = False
                                #print(df.loc[i, title[p]])
                                for u in range(len(guige1)):
                                    if isinstance(df.loc[i, guige1[u]], str):
                                        #print(df.loc[i, guige1[u]])
                                        df.loc[i, guige1[u]] = df.loc[i, guige1[u]].replace(u'\xa0', u' ')
                                        for k in range(len(df.loc[i, guige1[u]].split(' '))):
                                            #print(df.loc[i, guige1[u]].split(' '))
                                            df_pool_all = ''
                                            for v in range(df_pool.loc[j,guige2].count()):
                                                df_pool_all += str(df_pool.loc[j, guige2[v]])

                                            #print(df.loc[i, guige1[u]].split(' ')[k])
                                            #print(df_pool_all)
                                            if df.loc[i, guige1[u]].split(' ')[k].strip() not in df_pool_all:
                                                name2 = True
                                                df_title_diff.loc[i] = df.loc[i]
                                if name2 == False:
                                    df.loc[i, '商品id'] = df_pool.loc[j, '商品id']
                                    df_title_same.loc[i] = df.loc[i]

        if name1 == False:
            df.loc[i, '商品名称判断'] = '是'
            df_title_diff.loc[i] = df.loc[i]

   #print(len(df_title_diff),len(df_title_same))
    return (df_title_same, df_title_diff)

def same_url_zd_judge(filePath):
    filename = get_filename(filePath + '相同链接数据提取/')
    #print(filename)
    for name in filename:
        df = same_zd_judge(filePath,name)
        '''if os.path.isfile(filePath + '不是新品/' + name):
            os.remove(filePath + '不是新品/' + name)
        if os.path.isfile(filePath + '需手动确认的新品/'+ name):
            os.remove(filePath + '需手动确认的新品/'+ name)'''
        df[0].to_excel(filePath + '不是新品/' + name,index=False)
        df[1].to_excel(filePath + '需手动确认的新品/' + name, index=False)

def diff_url_zd_judge(filePath):
    filename = get_filename(filePath + '不同链接数据提取/')
    # print(filename)
    for name in filename:
        df = diff_zd_judge(filePath, name)
        if os.path.isfile(filePath + '不是新品diff_url/' + name):
            os.remove(filePath + '不是新品diff_url/' + name)
        if os.path.isfile(filePath + '需手动确认的新品diff_url/' + name):
            os.remove(filePath + '需手动确认的新品diff_url/' + name)
        df[0].to_excel(filePath + '不是新品diff_url/' + name, index=False)
        df[1].to_excel(filePath + '需手动确认的新品diff_url/' + name, index=False)

def url_pool(fpath1 , fpath2):
    print(os.listdir(fpath2 + '提取数据1/'))
    for path in os.listdir(fpath2 + '提取数据1/'):
        df1 =  pd.read_excel(fpath1 + '提取数据1/' + path)
        print(len(df1))
        df2 = pd.read_excel(fpath2 + '提取数据1/'+ path)
        df = pd.concat([df2,df1])
        #df = df.reset_index(drop=True)
        df = df.reset_index(drop=True)
        idd = []
        print(len(df))

        for i in range(len(df)):
            if re.search('tmall', df.loc[i, '页面网址']):
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
        df.to_excel(fpath2 + '提取数据1/'+ path , index = False)



filePath1 = r'E:/01复硕正态/08项目/01沐浴露监测/01测试数据/01旗舰店数据/2018-3-31旗舰店数据/'
filePath2 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2018-2-28/'
filePath3 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2018-3-31/'
filePath4 = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据/'

'''filePath1 = r'E:\01复硕正态\08项目\03男士面霜\01测试数据\第三版/'
filePath2 = r'E:\01复硕正态\08项目\03男士面霜\02成品数据\第二版/'
filePath3 = r'E:\01复硕正态\08项目\03男士面霜\02成品数据\第三版/'
filePath4 = r'E:\01复硕正态\08项目\03男士面霜\02成品数据/'''
def main():
    word = ['天猫/', '京东/']
    #word = ['京东/']
    for name in word:
        # read_gz(filePath1 + name, filePath3 + name)
        # extract_data(filePath3 + name)
        # new_url_judge(filePath2 + name, filePath3 + name)
        # same_url_zd_judge(filePath3 + name)
        # diff_url_zd_judge(filePath3+name)
        url_pool(filePath2 + name,filePath3 + name)

if __name__ == '__main__':
    main()
    #same_url_zd_judge(filePath3+'京东/')