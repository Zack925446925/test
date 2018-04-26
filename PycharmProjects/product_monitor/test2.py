# -*- encoding:utf-8 -*-
import sys
from google.cloud import vision
import io
import os

from google.cloud.vision import types
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:\01复硕正态\08项目\12google文字识别\My Project 44653-04ffef0e0ed6.json"
# client = vision.ImageAnnotatorClient()
#
# with io.open(r'E:\A_judge_pic\1.jpg', 'rb') as image_file:
#     content = image_file.read()
# image = types.Image(content=content)
# response = client.text_detection(image=image)
# labels = response.label_annotations
# print(response)
# print('***********************************')
# print(labels)

import wx
class MainWindow(wx.Frame):
    """We simply derive a new class of Frame."""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (200, 100))
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()    #创建位于窗口的底部的状态栏

        #设置菜单
        filemenu = wx.Menu()

        #wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
        filemenu.Append(wx.ID_ABOUT, u"关于", u"关于程序的信息")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, u"退出", u"终止应用程序")

        #创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, u"文件")
        self.SetMenuBar(menuBar)
        self.Show(True)

app = wx.App(False)
frame = MainWindow(None, title = u"记事本")
app.MainLoop()