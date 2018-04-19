# author shu huizhen

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
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# browser = webdriver.Chrome(chrome_options=chrome_options)
#browser = webdriver.PhantomJS()

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
# from datetimeshz import date_time
def date_time(delta=0):
    now = datetime.date.today()
    delta2 = datetime.timedelta(days=1)
    delta = datetime.timedelta(days=delta)
    n_days = now - delta2 - delta
    return (n_days.strftime('%Y-%m-%d'))


# import tesseract-ocr
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-ORC/tesseract.exe'
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


# 打开浏览器
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
        fileaccount = open(r"E:\01复硕正态\07数据清洗/account.txt")
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


def fun1(drive, name):
    if is_element_exist_xpath(drive,'//*[@id="auto_gsid_15"]/div[1]/ul/li[1]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[1]').click()
    elif is_element_exist_xpath(drive,'//*[@id="auto_gsid_15"]/div[2]/ul/li[1]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[1]').click()
    time.sleep(5)
    path = r"E:\01复硕正态\01数据爬取\06指数抓取\01百度指数/半年/"
    if not os.path.exists(path+name):
        os.mkdir(path+name)
    if not os.path.exists(path+name+'/whole'):
        os.mkdir(path+name+'/whole')
    if not os.path.exists(path+name+'/pc'):
        os.mkdir(path+name+'/pc')
    if not os.path.exists(path+name+'/mobile'):
        os.mkdir(path+name+'/mobile')
    if os.path.isfile(path + name + '/baidu_index.txt'):
        os.remove(path + name + '/baidu_index.txt')
    f = open(path + name + '/baidu_index.txt', 'a', encoding='utf-8')
    # handles = browser.window_handles
    # browser.switch_to_window(handles[-1])
    for i in range(2, 7, 4):
        for k in range(1, 3):
            if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
            elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/span').click()
            drive.find_element_by_xpath(
                '//*[@id="auto_gsid_18"]/ul/li[' + str(k) + ']/a[1]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/ul/li[' + str(k) + ']/a[6]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
            time.sleep(5)
            js = "var q=document.body.scrollHeight ;return(q)"
            Text_height = browser.execute_script(js)
            js1 = "var q=document.documentElement.scrollTop=" + str(int(Text_height / 2))
            browser.execute_script(js1)
            time.sleep(2)
            if os.path.isfile(path + name + r'\whole/' + name + '_wholeTrence_' + str(i + k) + ".png"):
                os.remove(path + name + r'\whole/' + name + '_wholeTrence_' + str(i + k) + ".png")
            browser.save_screenshot(path + name + r'\whole/' + name + '_wholeTrence_' + str(i + k) + ".png")
            f.write(str(2010 + i) + '：' + '  ' + name + '_wholeTrence_' + str(i + k) + ".png" + '\n')

    if is_element_exist_xpath(browser,'//*[@id="auto_gsid_15"]/div[2]/ul/li[2]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[2]').click()
    elif is_element_exist_xpath(browser,'//*[@id="auto_gsid_15"]/div[1]/ul/li[2]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[2]').click()
    time.sleep(2)
    for i in range(3, 12, 4):
        for k in range(1, 3):
            if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
            elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/ul/li[' + str(k) + ']/a[1]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/span').click()
            drive.find_element_by_xpath(
                '//*[@id="auto_gsid_20"]/ul/li[' + str(k) + ']/a[6]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
            time.sleep(5)
            js = "var q=document.body.scrollHeight ;return(q)"
            Text_height = browser.execute_script(js)
            js1 = "var q=document.documentElement.scrollTop=" + str(int(Text_height / 2))
            browser.execute_script(js1)
            time.sleep(2)
            if os.path.isfile(path + name + r'\pc/' + name + '_pcTrence_' + str(i + k) + ".png"):
                os.remove(path + name + r'\pc/' + name + '_pcTrence_' + str(i + k) + ".png")
            browser.save_screenshot(path + name + r'\pc/' + name + '_pcTrence_' + str(i + k) + ".png")
            f.write(str(2005 + i) + '：' + '  ' + name + '_pcTrence_' + str(i + k) + ".png" + '\n')
    if is_element_exist_xpath(browser,'//*[@id="auto_gsid_15"]/div[2]/ul/li[3]'):   
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[3]').click()
    elif is_element_exist_xpath(browser,'//*[@id="auto_gsid_15"]/div[1]/ul/li[3]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[3]').click()

    time.sleep(2)
    for i in range(2, 7, 4):
        for k in range(1, 3):
            if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
            elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/span').click()
            drive.find_element_by_xpath(
                '//*[@id="auto_gsid_18"]/ul/li[' + str(k) + ']/a[1]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/ul/li[' + str(k) + ']/a[6]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
            time.sleep(5)
            js = "var q=document.body.scrollHeight ;return(q)"
            Text_height = browser.execute_script(js)
            js1 = "var q=document.documentElement.scrollTop=" + str(int(Text_height / 2))
            browser.execute_script(js1)
            time.sleep(2)
            if os.path.isfile(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i + k) + ".png"):
                os.remove(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i + k) + ".png")
            browser.save_screenshot(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i + k) + ".png")
            f.write(str(2010 + i) + '：' + '  ' + name + '_mobilTrence_' + str(i + k) + ".png" + '\n')
    f.close()


def fun2(drive, name):
    path = r"E:\01复硕正态\01数据爬取\06指数抓取\01百度指数\半年/"
    if not os.path.exists(path+name):
        os.mkdir(path+name)
    if not os.path.exists(path+name+'/whole'):
        os.mkdir(path+name+'/whole')
    if not os.path.exists(path+name+'/pc'):
        os.mkdir(path+name+'/pc')
    if not os.path.exists(path+name+'/mobile'):
        os.mkdir(path+name+'/mobile')
    if os.path.isfile(path + name + '/baidu_index.txt'):
        os.remove(path + name + '/baidu_index.txt')
    f = open(path + name + '/baidu_index.txt', 'a', encoding='utf-8')
    for i in range(2, 7, 4):
        for k in range(1, 3):
            if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
            elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[1]/span[2]/span[1]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[1]/span[2]/span[2]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/ul/li[' + str(k) + ']/a[1]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[2]/span[2]/span[1]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[2]/span[2]/span[2]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/ul/li[' + str(k) + ']/a[6]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
            time.sleep(5)
            js = "var q=document.body.scrollHeight ;return(q)"
            Text_height = browser.execute_script(js)
            js1 = "var q=document.documentElement.scrollTop=" + str(int(Text_height / 2))
            browser.execute_script(js1)
            time.sleep(2)
            if os.path.isfile(path + name + r'\whole/' + name + '_wholeTrence_' + str(i + k) + ".png"):
                os.remove(path + name + r'\whole/' + name + '_wholeTrence_' + str(i + k) + ".png")
            browser.save_screenshot(path + name + r'\whole/' + name + '_wholeTrence_' + str(i + k) + ".png")
            # js2 = "var q=document.documentElement.scrollTop=0"
            # browser.execute_script(js2)
            f.write(str(2010 + i) + '：' + '  ' + name + '_wholeTrence_' + str(i + k) + ".png" + '\n')
    if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/ul/li[2]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[2]').click()
        time.sleep(2)
    elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/ul/li[2]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[2]').click()
        time.sleep(2)
    for i in range(3, 12, 4):
        for k in range(1, 3):
            if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
            elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/ul/li[' + str(k) + ']/a[1]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/span').click()
            drive.find_element_by_xpath(
                '//*[@id="auto_gsid_20"]/ul/li[' + str(k) + ']/a[6]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
            time.sleep(5)
            js = "var q=document.body.scrollHeight ;return(q)"
            Text_height = browser.execute_script(js)
            js1 = "var q=document.documentElement.scrollTop=" + str(int(Text_height / 2))
            browser.execute_script(js1)
            time.sleep(2)
            if os.path.isfile(path + name + r'\pc/' + name + '_pcTrence_' + str(i + k) + ".png"):
                os.remove(path + name + r'\pc/' + name + '_pcTrence_' + str(i + k) + ".png")
            browser.save_screenshot(path + name + r'\pc/' + name + '_pcTrence_' + str(i + k) + ".png")
            # js2 = "var q=document.documentElement.scrollTop=0"
            # browser.execute_script(js2)
            f.write(str(2005 + i) + '：' + '  ' + name + '_pcTrence_' + str(i + k) + ".png" + '\n')
    if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/ul/li[3]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[3]').click()
        time.sleep(2)
    elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/ul/li[3]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[3]').click()
        time.sleep(2)
    for i in range(2, 7, 4):
        for k in range(1, 3):
            if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
            elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
                drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/span').click()
            drive.find_element_by_xpath(
                '//*[@id="auto_gsid_18"]/ul/li[' + str(k) + ']/a[1]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i) + ']').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/span').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/ul/li[' + str(k) + ']/a[6]').click()
            drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
            time.sleep(5)
            js = "var q=document.body.scrollHeight ;return(q)"
            Text_height = browser.execute_script(js)
            js1 = "var q=document.documentElement.scrollTop=" + str(int(Text_height / 2))
            browser.execute_script(js1)
            time.sleep(2)
            if os.path.isfile(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i + k) + ".png"):
                os.remove(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i + k) + ".png")
            browser.save_screenshot(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i + k) + ".png")
            # js2 = "var q=document.documentElement.scrollTop=0"
            # browser.execute_script(js2)
            f.write(str(2010 + i) + '：' + '  ' + name + '_mobilTrence_' + str(i + k) + ".png" + '\n')
    f.close()


def fun(drive, name):
    path = r"E:\01复硕正态\01数据爬取\06指数抓取\01百度指数\整年/"
    if not os.path.exists(path+name):
        os.mkdir(path+name)
    if not os.path.exists(path+name+'/whole'):
        os.mkdir(path+name+'/whole')
    if not os.path.exists(path+name+'/pc'):
        os.mkdir(path+name+'/pc')
    if not os.path.exists(path+name+'/mobile'):
        os.mkdir(path+name+'/mobile')
    if os.path.isfile(path + name + '/baidu_index.txt'):
        os.remove(path + name + '/baidu_index.txt')
    f = open(path + name + '/baidu_index.txt', 'a', encoding='utf-8')
    for i in range(7):
        if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
            drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
        elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
            drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[1]/span[2]/span[1]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i + 1) + ']').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[1]/span[2]/span[2]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/ul/li[1]/a[1]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[2]/span[2]/span[1]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i + 1) + ']').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[2]/span[2]/span[2]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/ul/li[2]/a[6]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
        time.sleep(5)
        js1 = "var q=document.documentElement.scrollTop=10000"
        browser.execute_script(js1)
        time.sleep(2)
        if os.path.isfile(path + name + r'\whole/' + name + '_wholeTrence_' + str(i) + ".png"):
            os.remove(path + name + r'\whole/' + name + '_wholeTrence_' + str(i) + ".png")
        browser.save_screenshot(path + name + r'\whole/' + name + '_wholeTrence_' + str(i) + ".png")
        js2 = "var q=document.documentElement.scrollTop=0"
        browser.execute_script(js2)
        f.write(str(2011 + i) + '：' + '  ' + name + '_wholeTrence_' + str(i) + ".png" + '\n')
    if is_element_exist_xpath(browser,'//*[@id="auto_gsid_15"]/div[2]/ul/li[2]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[2]').click()
    elif is_element_exist_xpath(browser,'//*[@id="auto_gsid_15"]/div[1]/ul/li[2]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[2]').click()
    time.sleep(2)
    for i in range(12):
        if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
            drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
        elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
            drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i + 1) + ']').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/span').click()
        if i == 0:
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/ul/li[1]/a[6]').click()
        else:
            drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/ul/li[1]/a[1]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i + 1) + ']').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/ul/li[2]/a[6]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
        time.sleep(5)
        js1 = "var q=document.documentElement.scrollTop=10000"
        browser.execute_script(js1)
        time.sleep(2)
        if os.path.isfile(path + name + r'\pc/' + name + '_pcTrence_' + str(i) + ".png"):
            os.remove(path + name + r'\pc/' + name + '_pcTrence_' + str(i) + ".png")
        browser.save_screenshot(path + name + r'\pc/' + name + '_pcTrence_' + str(i) + ".png")
        js2 = "var q=document.documentElement.scrollTop=0"
        browser.execute_script(js2)
        f.write(str(2006 + i) + '：' + '  ' + name + '_pcTrence_' + str(i) + ".png" + '\n')
    if is_element_exist_xpath(browser,'//*[@id="auto_gsid_15"]/div[1]/ul/li[3]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/ul/li[3]').click()
    elif is_element_exist_xpath(browser,'//*[@id="auto_gsid_15"]/div[2]/ul/li[3]'):
        drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/ul/li[3]').click()
    time.sleep(2)
    for i in range(7):
        if is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]'):
            drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[1]/div[1]/a[7]').click()
        elif is_element_exist_xpath(drive, '//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]'):
            drive.find_element_by_xpath('//*[@id="auto_gsid_15"]/div[2]/div[1]/a[7]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_17"]/div/a[' + str(i + 1) + ']').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_18"]/ul/li[1]/a[1]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_19"]/div/a[' + str(i + 1) + ']').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/span').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_20"]/ul/li[2]/a[6]').click()
        drive.find_element_by_xpath('//*[@id="auto_gsid_16"]/div[3]/input[1]').click()
        time.sleep(5)
        js1 = "var q=document.documentElement.scrollTop=10000"
        browser.execute_script(js1)
        time.sleep(2)
        if os.path.isfile(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i) + ".png"):
            os.remove(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i) + ".png")
        browser.save_screenshot(path + name + r'\mobile/' + name + '_mobilTrence_' + str(i) + ".png")
        js2 = "var q=document.documentElement.scrollTop=0"
        browser.execute_script(js2)
        f.write(str(2011 + i) + '：' + '  ' + name + '_mobilTrence_' + str(i) + ".png" + '\n')
    f.close()


def get_index_pic(filepath1, filepath2):
    for nm1 in os.listdir(filepath1):
        fpath = filepath1 + nm1 + '/'
        fpath1 = filepath2 + nm1 + '/'
        for nm2 in os.listdir(fpath):
            im = Image.open(fpath + nm2)
            for i in range(im.size[1]):
                if im.getpixel((im.size[0] / 2, i)) == (221, 221, 221):
                    dm = i
                    break
            rangle = (185, dm, 1729 - (185 - 162), dm + 70 + 7 * 37)
            if os.path.isfile(fpath1 + nm2):
                os.remove(fpath1 + nm2)
            im.crop(rangle).save(fpath1 + nm2)



import pandas as pd
df = pd.read_excel(r'E:\01复硕正态\01数据爬取\06指数抓取/采集关键词.xlsx')
for word in df['关键字'].values:
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
    keyword = word
    browser.find_element_by_id("schword").clear()
    # 写入需要搜索的百度指数
    browser.find_element_by_id("schword").send_keys(keyword)
    browser.find_element_by_id("searchWords").click()
    time.sleep(2)
    # 最大化窗口
    handles = browser.window_handles
    browser.switch_to_window(handles[-1])
    browser.maximize_window()
    if is_element_exist(browser, 'TANGRAM_12__userName'):  # browser.find_element_by_id("TANGRAM_12__userName"):
        account = []
        try:
            fileaccount = open(r"E:\01复硕正态\01数据爬取\06指数抓取\01百度指数/account.txt")
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
    print(keyword)
    fun(browser,keyword)
    fun1(browser, keyword)
    #fun2(browser,keyword)
browser.close()

