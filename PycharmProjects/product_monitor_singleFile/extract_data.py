# -*- encoding:utf-8 -*-
import xlrd
import pandas as pd
import numpy as np
from xlutils.copy import copy
path1 = r'E:/01复硕正态/08项目/01沐浴露监测/01测试数据/01旗舰店数据/2017-11-1旗舰店数据/合并/玉兰油.xls'
path2 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2017-11-1/元数据/玉兰油.xls'
path3 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2017-11-1/元数据/玉兰油.tq.xls'
writer = pd.ExcelWriter(path3)

def extract_data(path2,num):
    data = xlrd.open_workbook(path2)
    table = data.sheets()[num]
    nrows = table.nrows
    ncols = table.ncols

    xinhao1 = []
    for p in range(ncols):
        if table.cell(0, p).value == '页面网址':
            dprank = p
            #            print(dprank)
    for i in range(1, nrows):
    #if table.cell(i, dprank).value not in xinhao:
        chanping = {table.cell(0, dprank).value: table.cell(i, dprank).value.strip()}
        for j in range(dprank):
            chanping[table.cell(0, j).value] = table.cell(i, j).value.strip()
        #xinhao.append(table.cell(i, dprank).value)
        xinhao1.append(chanping)
        #            with open('E:/01复硕正态/07数据清洗/01成品数据/2017-10-25沐浴露/六神修改','a+') as f:
        #                f.write(str(chanping) + '\n')
        #            print(chanping)
    df = pd.DataFrame(xinhao1)
    df.to_excel(writer, index = False, sheet_name = str(num))
    writer.save('sss.xls')
def tmget(path1):
    data = xlrd.open_workbook(path1)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols

    dprank = 0
    ppmrank = 0
    ggrank = 0
    #复制一个用于写入的文件
    wb = copy(data)
    ws = wb.get_sheet(0)
    #print(table.cell(0,0).value)
    #从原表格中获取其他信息写入新表格
    for i in range(1,nrows):
        for p in range(ncols):
            if table.cell(0,p).value == '单品':
                dprank = p
            elif table.cell(0,p).value == '品牌名':
                ppmrank = p
            elif table.cell(0,p).value == '规格':
                ggrank = p

            if '型号:' in table.cell(i,p).value:
                xinhao = table.cell(i,p).value.split(':')
                #print (xinhao)
                if xinhao[1]:
                    ws.write(i,dprank, xinhao[1])
            elif '品牌:' in table.cell(i,p).value:
                chanpname = table.cell(i,p).value.split(':')
                #print(chanpname)
                if chanpname[1]:
                    ws.write(i,ppmrank, chanpname[1])
            elif '净含量:' in table.cell(i,p).value:
                guiges = table.cell(i,p).value.split(':')
                print (guiges)
                if guiges:
                    ws.write(i,ggrank, guiges[1])
    print(ggrank)
    wb.save('E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2017-11-1/元数据/玉兰油.xls')

def jdget(path1):
    data = xlrd.open_workbook(path1)
    table = data.sheets()[1]
    nrows = table.nrows
    ncols = table.ncols

    ggrank = 0
    #复制一个用于写入的文件
    wb = copy(data)
    ws = wb.get_sheet(1)
    #print(table.cell(0,0).value)
    #从原表格中获取其他信息写入新表格
    for i in range(nrows):
        for p in range(ncols):
            if table.cell(0,p).value == '规格':
                ggrank = p
            if '商品毛重：' in table.cell(i,p).value:
                #print (table.cell(i,p).value)
                guiges = table.cell(i,p).value.split('：')
                #print(guiges)
                if guiges[1]:
                    ws.write(i,ggrank, guiges[1])
    wb.save('E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2017-11-1/元数据/玉兰油.xls')
def main():
    tmget(path1)
    jdget(path2)
    #for i in range(2):

        #extract_data(i)

if __name__ == '__main__':
    main()