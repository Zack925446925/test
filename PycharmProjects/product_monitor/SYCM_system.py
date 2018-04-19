import pandas as pd
import xlrd
import time
from datetime import datetime
from xlutils.copy import copy

def fun1(pinlei,pingtai,Time):
    try:
        data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
        df0 = df_hangye.copy()
        df0['日期'] = df0['日期'].apply(judge_time_type())
        df0['date_index'] = df0['日期']
        df0 = df0.set_index('date_index')
        wb = copy(data)
        sheet = wb.get_sheet(0)
        df1 = df0[df0['品类'] == pinlei]
        df2 = df1[df1['平台'] == pingtai]
        df3 = df2[Time]
        for i in range(len(df3)):
            sheet.write(0, i + 1, df3.loc[df3.index[i], '日期'].strftime('%Y-%m'))
            sheet.write(1, i + 1, df3.loc[df3.index[i], '支付金额较父类目占比'])
            #print(df3.loc[df3.index[i], '日期'], df3.loc[df3.index[i], '支付金额较父类目占比'])
        wb.save(fpath1 + 'PPT最终数据.xls')
    except Exception as e:
        print(e)
def fun2(pinlei,pingtai,*date):#date为需要计算的年份，str
    try:
        data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
        df0 = df_hangye.copy()
        df0['日期'] = df0['日期'].apply(judge_time_type)
        df0['date_index'] = df0['日期']
        df0 = df0.set_index('date_index')
        wb = copy(data)
        sheet = wb.get_sheet(1)
        df1 = df0[df0['品类'] == pinlei]
        df2 = df1[df1['平台'] == pingtai]
        for i in range(len(date)):
            df3 = df2[date[i]]
            sheet.write(i + 1, 1, df3['交易指数'].sum())
            sheet.write(i + 1, 0, date[i - 1])
        wb.save(fpath1 + 'PPT最终数据.xls')
    except Exception as e:
        print(e)
def fun3(pinlei,pingtai,*date):

    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_hangye.copy()
    df0['日期'] = df0['日期'].apply(judge_time_type)
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(2)

    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    print(df2)
    print(date)
    for i in range(len(date)):
        df3 = df2[date[i]].sort_values(by='日期',ascending=True)
        sheet.write(2*i+1, 0, date[i])
        print(df3)
        for j in range(len(df3)):
            sheet.write(2*i, j + 1, df3.index[j].strftime('%Y-%m'))
            sheet.write(2*i+1, j+1, int(df3['交易指数'][df3.index[j]]))

    wb.save(fpath1 + 'PPT最终数据.xls')

def fun4(pinlei, pingtai,*date):
    try:
        data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
        df0 = df_shuxing.copy()
        df0['日期'] = df0['日期'].apply(judge_time_type)
        df0['date_index'] = df0['日期']
        df0 = df0.set_index('date_index')
        wb = copy(data)
        sheet = wb.get_sheet(3)
        df1 = df0[df0['品类'] == pinlei]
        df2 = df1[df1['平台'] == pingtai]
        df2 = df2[df2['属性'] == '功效']
        for i in range(len(date)):
            df3 = df2[date[i]].groupby('属性值').sum().sort_values(by='交易指数',ascending=False)
            sheet.write(2 * i + 1, 0, date[i])
            for j in range(len(df3)):
                sheet.write(2 * i, j + 1, df3.index[j])
                sheet.write(2 * i + 1, j + 1, int(df3['交易指数'][df3.index[j]]))
        wb.save(fpath1 + 'PPT最终数据.xls')
    except Exception as e:
        print(e)

def fun5(pinlei, pingtai,*date):
    try:
        data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
        df0 = df_shuxing.copy()
        df0['日期'] = df0['日期'].apply(judge_time_type)
        df0['date_index'] = df0['日期']
        df0 = df0.set_index('date_index')
        wb = copy(data)
        sheet = wb.get_sheet(4)
        df1 = df0[df0['品类'] == pinlei]
        df2 = df1[df1['平台'] == pingtai]
        df2 = df2[df2['属性'] == '净含量']
        for i in range(len(date)):
            df3 = df2[date[i]].groupby('属性值').sum().sort_values(by='交易指数', ascending=False)
            sheet.write(2 * i + 1, 0, date[i])
            for j in range(len(df3)):
                sheet.write(2 * i, j + 1, df3.index[j])
                sheet.write(2 * i + 1, j + 1, int(df3['交易指数'][df3.index[j]]))
        wb.save(fpath1 + 'PPT最终数据.xls')
    except Exception as e:
        print(e)
def judge_time_type(s):
    if s:
        if isinstance(s,int) or isinstance(s,str) or isinstance(s,float):
            s = pd.to_datetime(s,format='%Y-%m-%d %H:%M:%S')
    return s
def fun6(pinlei, pingtai,new_time,old_time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_pinpai.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(5)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[new_time]
    new_time_unique = list(set(df2_new['日期']))
    new_pinpai_data = {} #存储新的一年中按月分组后，各品牌的交易指数，品牌名称为键，交易指数为值，（嵌套字典）
    new_value_sort = {}  #存储新的一年中按月分组后各品牌交易指数，交易指数从大到小排序，（字典）
    for i in range(len(new_time_unique)):
        new_pinpai_data_month = {}
        for j in range(len(df2_new ['日期'])):
            if new_time_unique[i] == df2_new['日期'][j]:
                new_pinpai_data_month[df2_new['品牌名称'][j]] = df2_new ['交易指数'][j]
        new_value_sort[new_time_unique[i].strftime('%Y-%m-%d')] = sorted(new_pinpai_data_month.values(),reverse=True)
        new_pinpai_data[new_time_unique[i].strftime('%Y-%m-%d')] =  new_pinpai_data_month
    df2_old = df2[old_time]
    old_time_unique = list(set(df2_old['日期']))
    old_pinpai_data = {}#存储上一年中按月分组后，各品牌的交易指数，品牌名称为键，交易指数为值，（嵌套字典）
    #old_value_sort = {}#存储上一年中按月分组后各品牌交易指数，交易指数从大到小排序，（字典）
    for i in range(len(old_time_unique)):
        old_pinpai_data_month = {}
        for j in range(len(df2_old['日期'])):
            if old_time_unique[i] == df2_old['日期'][j]:
                old_pinpai_data_month[df2_old['品牌名称'][j]] = df2_old['交易指数'][j]
        #old_value_sort[new_time_unique[i].strftime('%Y-%m-%d')] = sorted(old_pinpai_data_month.values(), reverse=True)
        old_pinpai_data[old_time_unique[i].strftime('%Y-%m-%d')] = old_pinpai_data_month
    old_pinpai_month_data = []
    for month in old_pinpai_data.keys():
        old_pinpai_month_data.append(datetime.strptime(month, "%Y-%m-%d").month)
    new_pinpai_top_30 = {}#}#存储新的一年中按月分组后排名前30的各品牌名称，对应交易指数从大到小排序，（字典）
    for key in new_pinpai_data:
        new_pinpai_month_top_30 = []
        for value in range(30):
            new_pinpai_month_top_30.append(get_dic_key(new_pinpai_data[key],new_value_sort[key][value]))
        new_pinpai_top_30[key] = new_pinpai_month_top_30
    df_new_top_30 = pd.DataFrame(columns=new_pinpai_top_30.keys())
    all_pinpai_name = []
    for key in new_pinpai_top_30:
        df_new_top_30[key] = new_pinpai_top_30[key]
        all_pinpai_name.extend(new_pinpai_top_30[key])
    all_pinpai_name = list(set(all_pinpai_name))
    remove_pinpai = []
    for name in all_pinpai_name:
        for col in df_new_top_30.columns:
            if name not in df_new_top_30[col].values:
                remove_pinpai.append(name)
                break
    choose_pinpai_name = list(set(all_pinpai_name) - set(remove_pinpai))

    if len(choose_pinpai_name)>20:
        choose_pinpai_name_final = {}
        for name in choose_pinpai_name:
            all_value = 0
            for date in new_pinpai_data:
                all_value += new_pinpai_data[date][name]
            mean_value = all_value / len(new_pinpai_data)
            choose_pinpai_name_final[name] = mean_value
        choose_pinpai_name_final_sort = sorted(choose_pinpai_name_final.values(), reverse=True)[:,20]
        choose_pinpai_name_final_final = []
        for value in choose_pinpai_name_final_sort:
            choose_pinpai_name_final_final.append(get_dic_key(choose_pinpai_name_final,value))
        choose_pinpai_name = choose_pinpai_name_final_final.copy()

    num = len(choose_pinpai_name)
    for i in range(len(df_new_top_30.columns)):
        for j in range(num):
            if datetime.strptime(df_new_top_30.columns[i], "%Y-%m-%d").month in old_pinpai_month_data:
                old_date = df_new_top_30.columns[i].replace(str(datetime.strptime(df_new_top_30.columns[i], "%Y-%m-%d").year),str(datetime.strptime(df_new_top_30.columns[i],  "%Y-%m-%d").year - 1))
                #print(old_date)
                sheet.write(j + 1 + i * num, 0, df_new_top_30.columns[i])
                sheet.write(j + 1 + i * num, 1, choose_pinpai_name[j])
                new_jyzs = new_pinpai_data[df_new_top_30.columns[i]][choose_pinpai_name[j]]
                if choose_pinpai_name[j] not in old_pinpai_data[old_date].keys():
                    sheet.write(j + 1 + i * num, 2, 'xxx')
                    sheet.write(j + 1 + i * num, 3, new_jyzs)
                else:
                    old_jyzs = old_pinpai_data[old_date][choose_pinpai_name[j]]
                    sheet.write(j + 1 + i * num, 2, (new_jyzs - old_jyzs) / old_jyzs)
                    sheet.write(j + 1 + i * num, 3, new_jyzs)
    wb.save(fpath1 + 'PPT最终数据.xls')
def fun7(pinlei, pingtai,Time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_pinpai.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(6)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    new_time_unique = list(set(df2_new['日期']))
    new_pinpai_data = {}  # 存储新的一年中按月分组后，各品牌的交易指数，品牌名称为键，交易指数为值，（嵌套字典）
    new_value_sort_top10 = {}  # 存储新的一年中按月分组后各品牌交易指数，交易指数从大到小排序，（字典）
    for i in range(len(new_time_unique)):
        new_pinpai_data_month = {}
        for j in range(len(df2_new['日期'])):
            if new_time_unique[i] == df2_new['日期'][j]:
                new_pinpai_data_month[df2_new['品牌名称'][j]] = df2_new['交易指数'][j]
        new_value_sort_top10[new_time_unique[i].strftime('%Y-%m-%d')] = sorted(new_pinpai_data_month.values(), reverse=True)[:10]
        new_pinpai_data[new_time_unique[i].strftime('%Y-%m-%d')] = new_pinpai_data_month
    df_describle = pd.DataFrame(new_value_sort_top10)
    df_describle['max'] = df_describle.max(1)
    df_describle['min'] = df_describle.min(1)
    df_describle['mean'] = df_describle.mean(1)
    df_describle = df_describle.sort_values(by='mean',ascending=False)
    for i in range(len(df_describle)):
        sheet.write(i + 1, 1, int(df_describle.loc[i, 'max']))
        sheet.write(i + 1, 2, int(df_describle.loc[i, 'min']))
        sheet.write(i + 1, 3, int(df_describle.loc[i, 'mean']))

    for i in range(len(new_value_sort_top10)):
        sheet.write(14, i + 3, list(new_value_sort_top10.keys())[i])
        for j in range(10):
            value = new_value_sort_top10[list(new_value_sort_top10.keys())[i]][j]
            sheet.write(j + 15, i + 3, value)
    wb.save(fpath1 + 'PPT最终数据.xls')

def fun8(pinlei, pingtai,Time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_pinpai.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(7)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    new_time_unique = list(set(df2_new['日期']))
    new_pinpai_data = {}  # 存储新的一年中按月分组后，各品牌的交易指数，品牌名称为键，交易指数为值，（嵌套字典）
    new_value_sort = {}  # 存储新的一年中按月分组后各品牌交易指数，交易指数从大到小排序，（字典）
    for i in range(len(new_time_unique)):
        new_pinpai_data_month = {}
        for j in range(len(df2_new['日期'])):
            if new_time_unique[i] == df2_new['日期'][j]:
                new_pinpai_data_month[df2_new['品牌名称'][j]] = df2_new['交易指数'][j]
        new_value_sort[new_time_unique[i].strftime('%Y-%m-%d')] = sorted(new_pinpai_data_month.values(), reverse=True)
        new_pinpai_data[new_time_unique[i].strftime('%Y-%m-%d')] = new_pinpai_data_month
    new_pinpai_top_30 = {}  # }#存储新的一年中按月分组后排名前30的各品牌名称，对应交易指数从大到小排序，（字典）
    for key in new_pinpai_data:
        new_pinpai_month_top_30 = []
        for value in range(30):
            new_pinpai_month_top_30.append(get_dic_key(new_pinpai_data[key], new_value_sort[key][i]))
        new_pinpai_top_30[key] = new_pinpai_month_top_30
    df_new_top_30 = pd.DataFrame(columns=new_pinpai_top_30.keys())
    all_pinpai_name = []
    for key in new_pinpai_top_30:
        df_new_top_30[key] = new_pinpai_top_30[key]
        all_pinpai_name.extend(new_pinpai_top_30[key])
    all_pinpai_name = list(set(all_pinpai_name))
    remove_pinpai = []
    for name in all_pinpai_name:
        for col in df_new_top_30.columns:
            if name not in df_new_top_30[col]:
                remove_pinpai.append(name)
                break
    choose_pinpai_name = list(set(all_pinpai_name)-set(remove_pinpai))
    if len(choose_pinpai_name)>20:
        choose_pinpai_name_final = {}
        for name in choose_pinpai_name:
            all_value = 0
            for date in new_pinpai_data:
                all_value += new_pinpai_data[date][name]
            mean_value = all_value / len(new_pinpai_data)
            choose_pinpai_name_final[name] = mean_value
        choose_pinpai_name_final_sort = sorted(choose_pinpai_name_final.values(), reverse=True)[:, 20]
        choose_pinpai_name_final_final = []
        for value in choose_pinpai_name_final_sort:
            choose_pinpai_name_final_final.append(get_dic_key(choose_pinpai_name_final, value))
        choose_pinpai_name = choose_pinpai_name_final_final.copy()

    df_top_20 = pd.DataFrame(columns=new_pinpai_top_30.keys())
    for i in range(len(choose_pinpai_name)):
        for j in range(len(df_top_20.columns)):
            df_top_20.loc[i, df_top_20.columns[j]] = new_pinpai_data[df_top_20.columns[j]][choose_pinpai_name[i]]
    df_top_20['max'] = df_top_20.max(1)
    df_top_20['min'] = df_top_20.min(1)
    df_top_20['mean'] = df_top_20.mean(1)
    df_top_20['品牌名称'] = choose_pinpai_name
    df_top_20 = df_top_20.sort_values(by='mean', ascending=False)
    df_top_20 = df_top_20.reset_index(drop=True)
    for j in range(len(new_pinpai_data)):
        sheet.write(23, 2 + j, df_top_20.columns[j])

    for i in range(len(df_top_20)):
        sheet.write(i + 1, 0, df_top_20.loc[i, '品牌名称'])
        sheet.write(i + 1, 1, df_top_20.loc[i, 'max'])
        sheet.write(i + 1, 2, df_top_20.loc[i, 'min'])
        sheet.write(i + 1, 3, df_top_20.loc[i, 'mean'])
        sheet.write(24 + i, 1, df_top_20.loc[i, '品牌名称'])
        for j in range(len(new_pinpai_data)):
            sheet.write(24 + i, 2 + j, df_top_20.iloc[i, j])
    wb.save(fpath1 + 'PPT最终数据.xls')

def fun9(pinlei, pingtai,Time):#Time为月份，如 ： '2017-8'
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_dianpu.copy()
    df0['开始日期'] = pd.to_datetime(df0['开始日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['开始日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(9)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    df2_new = df2_new[['店铺名称','交易指数']].groupby('店铺名称').sort_values(by='交易指数',ascending=False)
    for i in range(len(df2_new)):
        sheet.write(i+1,0,df2_new.index[i])
        sheet.write(i+1,1,df2_new['交易指数'][i])


def fun10(pinlei, pingtai,Time):#同fun7
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_danpin.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(6)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    new_time_unique = list(set(df2_new['日期']))
    new_pinpai_data = {}  # 存储新的一年中按月分组后，各品牌的交易指数，品牌名称为键，交易指数为值，（嵌套字典）
    new_value_sort_top10 = {}  # 存储新的一年中按月分组后各品牌交易指数，交易指数从大到小排序，（字典）
    for i in range(len(new_time_unique)):
        new_pinpai_data_month = {}
        for j in range(len(df2_new['日期'])):
            if new_time_unique[i] == df2_new['日期'][j]:
                new_pinpai_data_month[df2_new['品牌名称'][j]] = df2_new['交易指数'][j]
        new_value_sort_top10[new_time_unique[i].strftime('%Y-%m-%d')] = sorted(new_pinpai_data_month.values(),
                                                                               reverse=True)[:10]
        new_pinpai_data[new_time_unique[i].strftime('%Y-%m-%d')] = new_pinpai_data_month
    df_describle = pd.DataFrame(new_value_sort_top10)
    df_describle['max'] = df_describle.max(1)
    df_describle['min'] = df_describle.min(1)
    df_describle['mean'] = df_describle.mean(1)
    df_describle = df_describle.sort_values(by='mean', ascending=False)
    for i in range(len(df_describle)):
        sheet.write(i + 1, 1, int(df_describle.loc[i, 'max']))
        sheet.write(i + 1, 2, int(df_describle.loc[i, 'min']))
        sheet.write(i + 1, 3, int(df_describle.loc[i, 'mean']))

    for i in range(len(new_value_sort_top10)):
        sheet.write(14, i + 3, list(new_value_sort_top10.keys())[i])
        for j in range(10):
            value = new_value_sort_top10[list(new_value_sort_top10.keys())[i]][j]
            sheet.write(j + 15, i + 3, value)
    wb.save(fpath1 + 'PPT最终数据.xls')

def fun11(pinlei, pingtai,Time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_danpin.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(10)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    new_time_unique = list(set(df2_new['日期']))
    new_pinpai_data = {}  # 存储新的一年中按月分组后，各单品的交易指数，品牌名称为键，交易指数为值，（嵌套字典）
    new_value_sort = {}  # 存储新的一年中按月分组后各单品交易指数，交易指数从大到小排序，（字典）
    for i in range(len(new_time_unique)):
        new_pinpai_data_month = {}
        for j in range(len(df2_new['日期'])):
            if new_time_unique[i] == df2_new['日期'][j]:
                new_pinpai_data_month[df2_new['产品名称'][j]] = df2_new['交易指数'][j]
        new_value_sort[new_time_unique[i].strftime('%Y-%m-%d')] = sorted(new_pinpai_data_month.values(), reverse=True)
        new_pinpai_data[new_time_unique[i].strftime('%Y-%m-%d')] = new_pinpai_data_month
    for i in range(len(new_value_sort)):
        df_final = pd.DataFrame(columns=new_value_sort[i])
        df_final[new_value_sort[i]] = new_value_sort[new_value_sort[i]]
        value = df_final.head(50)[new_value_sort[i]].sum()/df_final[new_value_sort[i]].sum()
        sheet.write(i+1,0,new_value_sort[i])
        sheet.write(1+i,1,value)
        sheet.write(1+i,2,1-value)
    wb.save(fpath1 + 'PPT最终数据.xls')

def fun12(pinlei, pingtai,Time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_sex.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(13)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    new_time_unique = list(set(df2_new['日期']))
    for i in range(len(new_time_unique)):
        for j in range(len(df2_new)):
            if new_time_unique[i] == df2_new['日期'][j]:
                sheet.write(0, i + 1, new_time_unique[i].strftime('%Y-%m'))
                if df2_new['性别'][j] == '女':
                    sheet.write(1+j,i+1,df2_new['占比'][j])
                elif df2_new['性别'][j] == '男':
                    sheet.write(1+j,i + 1, df2_new['占比'][j])
                else:
                    sheet.write(1+j,i + 1, df2_new['占比'][j])
    wb.save(fpath1 + 'PPT最终数据.xls')

def fun13(pinlei, pingtai,Time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_age.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(13)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    new_time_unique = list(set(df2_new['日期']))
    for i in range(len(new_time_unique)):
        for j in range(len(df2_new)):
            if new_time_unique[i] == df2_new['日期'][j]:
                sheet.write(5, i + 1, new_time_unique[i].strftime('%Y-%m'))
                if df2_new['年龄'][j] == '18-25岁':
                    sheet.write(6+j,i+1,df2_new['占比'][j])
                elif df2_new['年龄'][j] == '26-30岁':
                    sheet.write(6+j,i + 1, df2_new['占比'][j])
                elif df2_new['年龄'][j] == '31-35岁':
                    sheet.write(6+j,i + 1, df2_new['占比'][j])
                elif df2_new['年龄'][j] == '36-40岁':
                    sheet.write(6+j,i + 1, df2_new['占比'][j])
                elif df2_new['年龄'][j] == '41-50岁':
                    sheet.write(6+j,i + 1, df2_new['占比'][j])
                elif df2_new['年龄'][j] == '51岁以上':
                    sheet.write(6+j,i + 1, df2_new['占比'][j])
                else:
                    sheet.write(6+j,i + 1, df2_new['占比'][j])
    wb.save(fpath1 + 'PPT最终数据.xls')

def fun14(pinlei, pingtai,Time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_work.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(13)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    new_time_unique = list(set(df2_new['日期']))
    for i in range(len(new_time_unique)):
        for j in range(len(df2_new)):
            if new_time_unique[i] == df2_new['日期'][j]:
                sheet.write(14, i + 1, new_time_unique[i].strftime('%Y-%m'))
                if df2_new['职业'][j] == '公司职员':
                    sheet.write(15+j, i +1,df2_new['占比'][j])
                elif df2_new['职业'][j] == '学生':
                    sheet.write(15+j, i  + 1, df2_new['占比'][j])
                elif df2_new['职业'][j] == '个体经营/服务人员':
                    sheet.write(15+j, i  + 1, df2_new['占比'][j])
                elif df2_new['职业'][j] == '教职工':
                    sheet.write(15+j, i  + 1, df2_new['占比'][j])
                elif df2_new['职业'][j] == '医务人员':
                    sheet.write(15+j, i  + 1, df2_new['占比'][j])
                elif df2_new['职业'][j] == '公务员':
                    sheet.write(15+j, i  + 1, df2_new['占比'][j])
                else:
                    sheet.write(15+j, i  + 1, df2_new['占比'][j])
    wb.save(fpath1 + 'PPT最终数据.xls')

def fun15(pinlei, pingtai,Time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_province.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(13)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    province_name = list(set(df2_new['省份']))
    new_time_unique = list(set(df2_new['日期']))
    for i in range(len(new_time_unique)):
        for j in range(len(df2_new)):
            if new_time_unique[i] == df2_new['日期'][j]:
                sheet.write(0, i + 15, new_time_unique[i].strftime('%Y-%m'))
                if df2_new['省份'][j] in province_name:
                    sheet.write(1+j, 14, df2_new['省份'][j])
                    sheet.write(1+j,15+i,df2_new['支付买家数占比'][j])
    wb.save(fpath1 + 'PPT最终数据.xls')

def fun16(pinlei, pingtai,Time):
    data = xlrd.open_workbook(fpath1 + 'PPT最终数据.xls')
    df0 = df_city.copy()
    df0['日期'] = pd.to_datetime(df0['日期'], format='%Y-%m-%d %H:%M:%S')
    df0['date_index'] = df0['日期']
    df0 = df0.set_index('date_index')
    wb = copy(data)
    sheet = wb.get_sheet(13)
    df1 = df0[df0['品类'] == pinlei]
    df2 = df1[df1['平台'] == pingtai]
    df2_new = df2[Time]
    city_name = list(set(df2_new['城市']))
    new_time_unique = list(set(df2_new['日期']))
    for i in range(len(new_time_unique)):
        for j in range(len(df2_new)):
            if new_time_unique[i] == df2_new['日期'][j]:
                sheet.write(23, i + 1, new_time_unique[i].strftime('%H-%m'))
                if df2_new['省份'][j] in city_name:
                    sheet.write(24+j, 0, df2_new['城市'][j])
                    sheet.write(24+j,i+1,df2_new['占比'][j])
    wb.save(fpath1 + 'PPT最终数据.xls')

#获取了每月的品牌排序数据，通过值找键        
def get_dic_key(dic,value):
    keys = ''
    for key in dic:
        if dic[key] == value:
            keys = key
    return keys

fpath1 = r'E:\01复硕正态\08项目\05生意参谋自动化\数据/'
df_hangye = pd.read_excel(fpath1 + '原始数据.xlsx')
df_shuxing = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=4)
df_pinpai = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=1)
df_dianpu = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=3)
df_danpin = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=2)
df_sex = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=5)
df_age = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=6)
df_work = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=7)
df_province = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=8)
df_city = pd.read_excel(fpath1 + '原始数据.xlsx',sheetname=9)
if __name__ == '__main__':
    #fun1('BB霜', '淘宝', '2017-9-1', '2017-8-1')
    #fun2('BB霜', '淘宝', '2017')
    #fun3('BB霜', '淘宝', '2017')
    fun4('男士BB霜', '全网', '2017')
    fun5('男士BB霜', '全网', '2017')