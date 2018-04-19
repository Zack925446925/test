import pandas as pd
import re
import numpy as np

df1 = pd.read_excel(r'E:\01复硕正态\07数据清洗\04客户名单匹配/客户名单.xlsx',sheetname=6)
df2 = pd.read_excel(r'E:\01复硕正态\07数据清洗\04客户名单匹配/化妆品品牌.xlsx')
def extract_chinese(s):
    for i in re.findall('[\da-zA-Z.\s*]*', s):
        if i:
            s = s.replace(i, '')
    return s
def extract_english(s):
    ss = ''
    for i in re.findall('[\da-zA-Z]*', s):
        ss = i + ss
    s = ss.upper()
    return s
extract_english('江原道 Koh Gen Do')

pinpai = []
for i in range(len(df1)):
    #print(df1.loc[i,'品牌'])
    if '/' in df1.loc[i,'品牌']:
        pinpai.append(df1.loc[i,'品牌'].split('/'))
    else:
        if re.search('[a-zA-Z]',df1.loc[i,'品牌']):
            pinpai.append([extract_chinese(df1.loc[i,'品牌']),extract_english(df1.loc[i,'品牌'])])
        else:
            pinpai.append([df1.loc[i,'品牌'],''])

pinpai1 = []
for i in range(len(df2)):
    #print(df1.loc[i,'品牌'])
    if '/' in df2.loc[i,'品牌名']:
        pinpai1.append(df2.loc[i,'品牌名'].split('/'))
    else:
        if re.search('[a-zA-Z]',df2.loc[i,'品牌名']):
            pinpai1.append([extract_chinese(df2.loc[i,'品牌名']),extract_english(df2.loc[i,'品牌名'])])
        else:
            pinpai1.append([df2.loc[i,'品牌名'],''])
print(pinpai)
print(pinpai1)
df3 = pd.DataFrame(columns=df2.columns)
for i in df2.columns:
    df1[i] = np.nan
kK = 0
for i in range(len(df2)):
    print(df2.loc[i, '品牌名'])
    flag = False
    for q in range(2):
        flag2=False
        if len(pinpai1[i][q])!=0:
            for j in range(len(df1)):
                flag1 = False
                for k in range(2):
                    flag3 = False
                    if len(pinpai[j][k].strip()) != 0:
                        #print(pinpai[j][k].strip())
                        ##print(df2.loc[i,'品牌名'])
                        if pinpai[j][k].strip() == pinpai1[i][q].strip():
                            print(pinpai[j][k].strip())
                            flag = True
                            flag1 = True
                            flag2 = True
                            flaag3 = True
                            df1.loc[j, df2.columns] = df2.loc[i].values
                            kK = kK + 1
                    if flag3:
                        break
            if flag1:
                break
        if flag2:
            break
    if flag == False:
        df3.loc[i] = df2.loc[i]
df1.to_excel(r'E:\01复硕正态\07数据清洗\04客户名单匹配/完成1.xlsx',index=False)
df3.to_excel(r'E:\01复硕正态\07数据清洗\04客户名单匹配/完成2.xlsx',index=False)
print(kK)
print(len(df3))
print(len(df2))
print(len(df1))
print(len(pinpai))