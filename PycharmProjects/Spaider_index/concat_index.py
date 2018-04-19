import re
import pandas as pd
import os
filepath1 = r'E:\01复硕正态\01数据爬取\06指数抓取\01百度指数\新建文件夹/'
#filepath1 = r'E:\01复硕正态\01数据爬取\06指数抓取\01百度指数\2018：1-3月/'
def fun1(fpath,s,dic):
    name = [i for i in s.split('_')]
    df = pd.read_excel(fpath+s)
    if re.match('whole',name[1]):
        df.columns = ['日期', '整体趋势指数值']
    elif re.match('pc',name[1]):
        df.columns = ['日期', 'PC趋势指数值']
    elif re.match('mobil',name[1]):
        df.columns = ['日期', '移动趋势指数值']
    df.drop([0], inplace=True)
    df = df.reset_index(drop=True)
    year = dic[s.replace('xls', 'png')]

    result = df['日期'].values
    #print(len(result))
    if len(df)-184 ==0:
        date = pd.date_range(year.strip()+'0701', periods=184)
        df['日期'] = date
        df['日期'] = df['日期'].apply(switch_time)
        df['热度关键词'] = name[0]
        return df
    else:
        for i in range(len(df) - 1):
            #print(result[i + 1] ,result[i])
            if abs(result[i + 1] - result[i]) <= 0.5:
                #print(i)
                #print(df.ix[i + 1, 1])
                df.ix[i + 1, 1] = (df.ix[i, 1] + df.ix[i + 1, 1]) / 2
                df.drop([i], inplace=True)
                #print(df)
        df = df.reset_index(drop=True)
        if len(df) == 184:
            date = pd.date_range('20170701', periods=184)
            df['日期'] = date
            df['日期'] = df['日期'].apply(switch_time)
            df['热度关键词'] = name[0]
            return df
        else:
            print(len(df))
            print('请检查{nm}'.format(nm=s))

    # df_num = len(df)
    # #num = len(df)-365
    # num = len(df)-90
    # if num < 0:
    #     for i in range(abs(num)):
    #         df.loc[df_num+i] = df.loc[df_num-1]
    # elif num > 0:
    #     for i in range(num):
    #         df.drop([df_num-i-1],inplace = True)
    # print(len(df))

    #return df
def switch_time(t):
    t = t.strftime("%Y-%m-%d").strip()
    return t
def fun2(fpath):
    year_fname = {}
    with open(fpath +'baidu_index.txt',encoding='utf-8') as f:
        for line in f.readlines():
            word = line.split('：')
            year_fname[word[1].strip()] = word[0]
    #print(year_fname)
    if not os.path.exists(fpath + '合并'):
        os.mkdir(fpath + '合并')
    for name in os.listdir(fpath):
        #print(name)
        if re.search('值',name):
            df = pd.DataFrame(columns=['日期', '整体趋势指数值', '热度关键词', 'PC趋势指数值', '移动趋势指数值'])
            for name1 in os.listdir(fpath+name+'/'):
                df = pd.concat([df,fun1(fpath+name+'/',name1,year_fname)],ignore_index=True)

            if os.path.isfile(fpath + '合并/' + name+'.xls'):
                os.remove(fpath + '合并/' + name+'.xls')
            df.to_excel(fpath + '合并/' + name+'.xls',index=False)

def fun3(fpath,fname):
    df1 = pd.read_excel(fpath+'合并/pc_值.xls')
    df2 = pd.read_excel(fpath + '合并/whole_值.xls')
    df3 = pd.read_excel(fpath + '合并/mobile_值.xls')
    for i in df1.columns:
        if df1[i].count() == 0:
            del df1[i]
    #print(df1)
    for i in df2.columns:
        if df2[i].count() == 0:
            del df2[i]
    #print(df2)
    for i in df3.columns:
        if df3[i].count() == 0:
            del df3[i]
    #print(df3)
    df0 = pd.merge(df1,df2, how='left',on=['日期','热度关键词'])
    df0 = pd.merge(df0, df3, how='left', on=['日期', '热度关键词'])
    if os.path.isfile(fpath + fname + '.xls'):
        os.remove(fpath + fname + '.xls')
    df0.to_excel(fpath + fname + '.xls',index=False)




if __name__ == '__main__':
    for name in os.listdir(filepath1):
        fun2(filepath1+name+'/')
        fun3(filepath1+name+'/',name)
    # fun2(filepath1+'男士面部护理/')
    # fun3(filepath1 + '男士面部护理/', '男士面部护理')

