from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract
import datetime
from selenium.webdriver.support import expected_conditions as EC
import os
import random
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# browser = webdriver.Chrome(chrome_options=chrome_options)
fpath = "./"
browser = webdriver.PhantomJS()
#browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
def openbrowser():
    # https://passport.baidu.com/v2/?login
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
    # 打开谷歌浏览器
    # Firefox()
    # Chrome()

    # 输入网址
    browser.get(url)
    if browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").is_displayed():
        browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
    # 打开浏览器时间
    # print("等待10秒打开浏览器...")
    # time.sleep(10)

    # 找到id="TANGRAM__PSP_3__userName"的对话框
    # 清空输入框
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

    # 输入账号密码
    # 输入账号密码
    account = []
    try:
        fileaccount = open("./account.txt")
        accounts = fileaccount.readlines()
        for acc in accounts:
            account.append(acc.strip())
        fileaccount.close()
    except Exception as err:
        print(err)
        input("请正确在account.txt里面写入账号密码")
        exit()
    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])

    # # 点击登陆登陆
    # # id="TANGRAM__PSP_3__submit"
    # browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

    # 等待登陆10秒
    # print('等待登陆10秒...')
    # time.sleep(10)
    if is_element_exist(browser,'TANGRAM__PSP_3__verifyCode'):
        time.sleep(2)
        aa = '11'
        input_yz = browser.find_element_by_id("TANGRAM__PSP_3__verifyCode")
        input_yz.clear()
        input_yz.send_keys(aa)
    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()
def is_element_exist_xpath(drive, s):
    flag = True
    try:
        if drive.find_element_by_xpath(s):
            return flag
    except Exception as e:
        flag = False
        return flag


def is_element_exist(drive, s):
    flag = True
    try:
        if drive.find_element_by_id(s):
            return flag
    except Exception as e:
        flag = False
        return flag

import pandas as pd

def fun_month(driver,name):
    path = fpath
    if not os.path.exists(path + name):
        os.mkdir(path + name)
    if not os.path.exists(path + name + '/whole'):
        os.mkdir(path + name + '/whole')
    if not os.path.exists(path + name + '/pc'):
        os.mkdir(path + name + '/pc')
    if not os.path.exists(path + name + '/mobile'):
        os.mkdir(path + name + '/mobile')
    if not os.path.exists(path + name + '/whole_值'):
        os.mkdir(path + name + '/whole_值')
    if not os.path.exists(path + name + '/pc_值'):
        os.mkdir(path + name + '/pc_值')
    if not os.path.exists(path + name + '/mobile_值'):
        os.mkdir(path + name + '/mobile_值')
    if os.path.isfile(path + name + '/baidu_index.txt'):
        os.remove(path + name + '/baidu_index.txt')
    f = open(path + name + '/baidu_index.txt', 'a', encoding='utf-8')
    driver.find_element_by_xpath('//*[@id="schword"]').clear()
    driver.find_element_by_xpath('//*[@id="schword"]').send_keys(name)
    driver.find_element_by_xpath('//*[@id="schsubmit"]').click()
    time.sleep(random.randint(3,5))
    if is_element_exist_xpath(driver,'//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
        driver.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
    elif is_element_exist_xpath(driver,'//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
        driver.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
    driver.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[1]/span[2]/span[2]').click()
    driver.find_element_by_xpath('//*[@id="auto_gsid_17"]/ul/li[1]/a[1]').click()
    driver.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[2]/span[2]/span[2]/span').click() #修改此处标签
    driver.find_element_by_xpath('//*[@id="auto_gsid_18"]/ul/li[1]/a[3]').click()
    driver.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()#修改此处标签
    time.sleep(5)
    js1 = "var q=document.documentElement.scrollTop=10000"
    browser.execute_script(js1)
    time.sleep(2)
    if os.path.isfile(path + name + r'\whole/' + name + '_wholeTrence_' +  ".png"):
        os.remove(path + name + r'\whole/' + name + '_wholeTrence_'  + ".png")
    browser.save_screenshot(path + name + r'\whole/' + name + '_wholeTrence_' + ".png")
    f.write(str(2018) + '：' + '  ' + name + '_wholeTrence_' +  ".png" + '\n')
    js2 = "var q=document.documentElement.scrollTop=0"
    browser.execute_script(js2)
    if is_element_exist_xpath(driver,'//*[@id="auto_gsid_15"]/div[1]/ul/li[2]'):
        driver.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[2]').click()
    elif is_element_exist_xpath(driver,'//*[@id="auto_gsid_15"]/div[2]/ul/li[2]'):
        driver.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[2]').click()
    time.sleep((2))
    #js1 = "var q=document.documentElement.scrollTop=10000"
    browser.execute_script(js1)
    if os.path.isfile(path + name + r'\pc/' + name + '_pcTrence_' + ".png"):
        os.remove(path + name + r'\pc/' + name + '_pcTrence_'  + ".png")
    browser.save_screenshot(path + name + r'\pc/' + name + '_pcTrence_'  + ".png")
    f.write(str(2018) + '：' + '  ' + name + '_pcTrence_' +".png" + '\n')
    #js2 = "var q=document.documentElement.scrollTop=0"
    browser.execute_script(js2)
    time.sleep((2))
    if is_element_exist_xpath(driver,'//*[@id="auto_gsid_15"]/div[2]/ul/li[3]'):
        driver.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[3]').click()
    elif is_element_exist_xpath(driver,'//*[@id="auto_gsid_15"]/div[1]/ul/li[3]'):
        driver.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[3]').click()
    # elif driver.find_element_by_xpath(driver,'//*[@id="auto_gsid_15"]/div[2]/ul/li[3]'):
    #     driver.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[3]').click()
    browser.execute_script(js1)
    if os.path.isfile(path + name + r'\mobile/' + name + '_mobilTrence_' +  ".png"):
        os.remove(path + name + r'\mobile/' + name + '_mobilTrence_' +  ".png")
    browser.save_screenshot(path + name + r'\mobile/' + name + '_mobilTrence_' + ".png")
    f.write(str(2018) + '：' + '  ' + name + '_mobilTrence_' +  ".png" + '\n')
    f.close()
def spider():
    df = pd.read_excel('./采集关键词.xlsx')
    openbrowser()
    # 新开一个窗口，通过执行js来新开一个窗口
    js = 'window.open("http://index.baidu.com");'
    browser.execute_script(js)
    # 新窗口句柄切换，进入百度指数
    # 获得当前打开所有窗口的句柄handles
    # handles为一个数组
    handles = browser.window_handles
    # print(handles)
    # 切换到当前最新打开的窗口
    browser.switch_to_window(handles[-1])
    # keyword = word
    browser.find_element_by_id("schword").clear()
    browser.find_element_by_id("schword").send_keys(df['关键字'].values[0])
    browser.find_element_by_id("searchWords").click()
    time.sleep(2)
    # 最大化窗口
    handles = browser.window_handles
    browser.switch_to_window(handles[-1])
    browser.maximize_window()
    if is_element_exist(browser, 'TANGRAM_12__userName'):  # browser.find_element_by_id("TANGRAM_12__userName"):
        account = []
        try:
            fileaccount = open("./account.txt")
            accounts = fileaccount.readlines()
            for acc in accounts:
                account.append(acc.strip())
            fileaccount.close()
        except Exception as err:
            print(err)
            input("请正确在account.txt里面写入账号密码")
            exit()

        browser.find_element_by_id("TANGRAM_12__userName").clear()
        browser.find_element_by_id("TANGRAM_12__userName").send_keys(account[0])
        browser.find_element_by_id("TANGRAM_12__password").clear()
        browser.find_element_by_id("TANGRAM_12__password").send_keys(account[1])
        time.sleep(2)
        browser.find_element_by_id("TANGRAM_12__submit").click()
    time.sleep(5)

    # 写入需要搜索的百度指数
    #fun_month(browser, df['关键字'].values[0])
    for keyword in df['关键字'].values:
        print(keyword)
        fun_month(browser, keyword)
        # fun1(browser, keyword)
        # fun2(browser,keyword)
    #browser.close()
spider()