# -*- encoding:utf-8 -*-
import re
import xlwt
import xlrd
from xlutils.copy import copy
import os

filePath1 = r'E:/01复硕正态/07数据清洗/02测试数据/2017-10-27/2017-09-吴-电商平台详情/电商平台详情/'
filePath2 = r'E:/01复硕正态/07数据清洗/01成品数据/2017-10-27/'

#获取文件夹下的文件名
def get_filename(path):
    files = os.listdir(path)
    return files

# 读取规则信息
def read_gz(filePath1, filePath2,name):
    data = xlrd.open_workbook(filename = filePath1 + name)
    #print(data.sheets())
    table = data.sheet_by_name('规则')
    nrows = table.nrows
    ncols = table.ncols
    # 规则sheet的第二行需为天猫规则
    tmget(filePath1,name, table.cell(1, 1).value, table.cell(1, 2).value)
    #    print(nrows)
    #    print(table.cell(0,0).value)
    for i in range(2, nrows):
        if '天猫' == table.cell(i, 0).value:
            print(table.cell(i, 0).value)
            tmget(filePath2 , name, table.cell(i, 1).value, table.cell(i, 2).value)
        elif '京东' == table.cell(i, 0).value:
            print(table.cell(i, 0).value)
            jdget(filePath2, name, table.cell(i, 1).value, table.cell(i, 2).value)
        elif '淘宝' == table.cell(i, 0).value:
            print(table.cell(i, 0).value)
            tbget(filePath2, name, table.cell(i, 1).value, table.cell(i, 2).value)

# 提取天猫规则数据
def tmget(filePath2,name, zdname, keyname):
    # self.button1.SetLabel("Clicked")
    data = xlrd.open_workbook(filename=filePath2+name)
    table = data.sheet_by_name('天猫')
    nrows = table.nrows
    ncols = table.ncols
    #print(filePath2, zdname, keyname)
    #    ggrank = 0
    # 复制一个用于写入的文件
    wb = copy(data)
    ws = wb.get_sheet(0)
    # print(table.cell(0,0).value)
    # 从原表格中获取其他信息写入新表格
    try:
        for i in range(1,nrows):
            for p in range(ncols):
                #if table.cell(0,p) != '页面网址':
                #    clean_messy_code(table.cell(i,p))
                if str(table.cell(0, p).value) == str(zdname):
                    dprank = p
                    #                   print(dprank)
                if keyname + ':' in str(table.cell(i, p).value):
                #    print(table.cell(i,p).value)
                    xinhao = table.cell(i, p).value.split(':')
                    if len(xinhao) > 1:
                        ws.write(i, dprank, xinhao[1])
        wb.save('E:/01复硕正态/07数据清洗/01成品数据/2017-10-27/' + name )
    except Exception as e:
        print(e)

# 提取京东规则数据
def jdget(filePath2,name, zdname, keyname):
    data = xlrd.open_workbook(filename=filePath2+name)
    table = data.sheet_by_name('京东')
    nrows = table.nrows
    ncols = table.ncols
    # 复制一个用于写入的文件
    wb = copy(data)
    ws = wb.get_sheet(1)
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

        wb.save(filePath2+name)
    except Exception as e:
        print(e)


# 提取1号店规则数据
def tbget(filePath2,name, zdname, keyname):
    data = xlrd.open_workbook(filename=filePath2 +name)
    table = data.sheet_by_name('淘宝')
    nrows = table.nrows
    ncols = table.ncols
    dprank = 0
    zprank = 0
    # 复制一个用于写入的文件
    wb = copy(data)
    ws = wb.get_sheet(2)
    # print(table.cell(0,0).value)
    # 从原表格中获取其他信息写入新表格
    try:
        for i in range(1, nrows):
            for p in range(ncols):
                #if table.cell(0,p) != '页面网址':
                 #   clean_messy_code(table.cell(i,p))
                if table.cell(0, p).value == zdname:
                    cprank = p
                if keyname + '：' in str(table.cell(i, p).value):
                    #                    print(table.cell(i,p).value)
                    chanpname = table.cell(i, p).value.split('：')
                    if len(chanpname) > 1:
                        ws.write(i, cprank, chanpname[1])
        wb.save(filePath2+name)
    except Exception as e:
        print(e)

#去除sheet中的‘？’
def clean_messy_code(sheet):
    if '?' in sheet:
        sheet = sheet.replace('？',' ')

def main():
  #  filePath1 = 'C:/Users/tange/Desktop/测试数据/2017-10-27/2017-09-吴-电商平台详情/宝宝防晒露.xls'
   # filePath2 = 'E:/01复硕正态/07数据清洗/01成品数据/2017-10-27/宝宝防晒露修改.xls'
  filename = get_filename(filePath1)
  for name in filename:
      read_gz(filePath1, filePath2 , name)


if __name__ == '__main__':
    main()
