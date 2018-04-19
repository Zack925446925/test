import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from selenium import webdriver
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def login(url='https://login.tmall.com/?redirectURL=https%3A%2F%2Fwww.tmall.com%2F'):
    browser = webdriver.Chrome()
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    browser.switch_to.frame('J_loginIframe')
    input1 = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="J_QRCodeLogin"]/div[5]/a[1]')))
    input1.click()
    account = []
    with open(r'C:\Users\tange\Desktop\自动批量截图\网页全屏截图/account.txt', 'r') as f:
        for line in f.readlines():
            account.append(line.strip())
    input2 = wait.until(
        EC.presence_of_element_located((By.ID, 'TPL_username_1')))
    input2.clear()
    input2.send_keys(account[0])
    browser.find_element_by_id('TPL_password_1').send_keys(account[1])
    browser.find_element_by_id('J_SubmitStatic').click()
    time.sleep(random.randint(2,4))
    browser.switch_to_default_content()
    return browser
def tm(url,fpath,name):
    browser = webdriver.Chrome()
    browser.get(url)
    browser.maximize_window()
    time.sleep(random.randint(2,4))
    url1 = browser.current_url
    if re.search('^https://login.tmall.com', url1):
        time.sleep(random.randint(8,12))
    # browser = webdriver.Ie()
    # browser = webdriver.PhantomJS()
    # js = 'window.open('+ url +');'
    # browser.execute_script(js)
    # handles = browser.window_handles
    # browser.switch_to_window(handles[-1])
    # time.sleep(random.randint(2,4))
    js = "var q=document.body.scrollHeight ;return(q)"
    Text_height = browser.execute_script(js)
    n = Text_height // 1000
    print(n)
    for i in range(int(n)):
        js = "var q=document.documentElement.scrollTop=" + str((i + 1) * 1000)
        browser.execute_script(js)
        time.sleep(0.5)
    browser.execute_script("var q=document.documentElement.scrollTop=1000000")
    time.sleep(random.randint(5, 10))
    # browser.execute_script("""
    #         (function () {
    #             var y = 0;
    #             var step = 100;
    #             window.scroll(0, 0);
    #
    #             function f() {
    #                 if (y < document.body.scrollHeight) {
    #                     y += step;
    #                     window.scroll(0, y);
    #                     setTimeout(f, 100);
    #                 } else {
    #                     window.scroll(0, 0);
    #                     document.title += "scroll-done";
    #                 }
    #             }
    #
    #             setTimeout(f, 1000);
    #         })();
    #     """)
    #
    # for i in range(30):
    #     if "scroll-done" in browser.title:
    #         break
    #     time.sleep(random.randint(5,10))
    res = browser.page_source
    soup = BeautifulSoup(res,'lxml')
    df = pd.DataFrame(columns=['产品名称', '图片介绍链接', '产品介绍文本', '图片介绍链接-待定', '是否有视频', '产品链接'])
    for i , img in enumerate(soup.select('#mainwrap #description img')):
        if '.jpg' in img['src']:
            df.loc[i,'图片介绍链接'] = img['src']
            print(img['src'])
        elif '.jpeg' in img['src']:
            df.loc[i, '图片介绍链接'] = img['src']
    df = df.reset_index(drop=True)
    df.loc[0,'产品名称'] = name
    print(soup.select('#mainwrap #description'))
    df.loc[0,'产品介绍文本'] = soup.select('#mainwrap #description')[0].text
    if soup.select('#mainwrap #J_DcTopRight .img'):
        if '.jpg' in soup.select('#mainwrap #J_DcTopRight .img')[0] or '.jpeg' in soup.select('#mainwrap #J_DcTopRight .img')[0]:
            print(soup.select('#mainwrap #J_DcTopRight .img'))
            df.loc[0,'图片介绍链接-待定'] = soup.select('#mainwrap #J_DcTopRight .img')[0]['src']
    df.loc[0,'产品链接'] = url
    if soup.select('#mainwrap #item-flash'):
        print(soup.select('#mainwrap #item-flash'))
        df.loc[0,'是否有视频'] = '是'
    if os.path.isfile(fpath + name + '.xlsx'):
        os.remove(fpath + name + '.xlsx')
    df.to_excel(fpath + name + '.xlsx', index=False)
    print('成功抓取：%s',name)

def spider_tm(fpath,date):
    if not os.path.exists(fpath + date):
        os.mkdir(fpath+date)
    df = pd.read_excel(fpath + '天猫产品链接.xlsx')
    fpath = fpath+date+'/'
    for  i,url in enumerate(df['链接'].values):
        tm(url,fpath,df.loc[i,'产品'])
def jd(url,fpath,name):
    #browser = webdriver.Chrome()
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(random.randint(4, 6))
    browser.execute_script("""
                (function () {
                    var y = 0;
                    var step = 100;
                    window.scroll(0, 0);

                    function f() {
                        if (y < document.body.scrollHeight) {
                            y += step;
                            window.scroll(0, y);
                            setTimeout(f, 100);
                        } else {
                            window.scroll(0, 0);
                            document.title += "scroll-done";
                        }
                    }

                    setTimeout(f, 1000);
                })();
            """)

    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(random.randint(5, 10))
    res = browser.page_source
    soup = BeautifulSoup(res, 'lxml')
    df = pd.DataFrame(columns=['产品名称','图片介绍链接','产品介绍文本','图片介绍链接-待定','是否有视频','产品链接'])
    if soup.select('#J-detail-content img'):
        ul = soup.select('#J-detail-content img')
        for i in range(len(ul)):
            df.loc[i, '图片介绍链接'] = 'https:' + ul[i]['src'].strip()
        if not soup.select('#J-detail-content style'):
            df.loc[0, '产品介绍文本'] = soup.select('#J-detail-content')[0].text.replace('\n', '')
        if soup.select('#activity_header img'):
            df.loc[0, '图片介绍链接-待定'] = soup.select('#activity_header img')[0]['src'].strip()
        if soup.select('.detail-content-wrap #tencent-video'):
            df.loc[0, '是否有视频'] = '是'
    else:
        ul = re.findall('url\(.*jpg', soup.select('#J-detail-content style')[0].text)
        for i in range(len(ul)):
            if re.search('https:',ul[i].strip()[4:]):
                df.loc[i, '图片介绍链接'] = ul[i].strip()[4:]
            else:
                df.loc[i, '图片介绍链接'] = 'https:' + ul[i].strip()[4:]
        if soup.select('#activity_header img'):
            df.loc[0, '图片介绍链接-待定'] = soup.select('#activity_header img')[0]
        if soup.select('.detail-content-wrap #tencent-video'):
            df.loc[0, '是否有视频'] = '是'
    df.loc[0,'产品名称'] = name
    df.loc[0,'产品链接'] = url
    print(df)
    if os.path.isfile(fpath+name+'.xlsx'):
        os.remove(fpath+name+'.xlsx')
    df.to_excel(fpath+name+'.xlsx',index=False)
def spider_jd(fpath,date,name):
    df = pd.read_excel(fpath+name)
    if not os.path.exists(fpath+date):
        os.mkdir(fpath+date)
    if not os.path.exists(fpath + date + '/京东'):
        os.mkdir(fpath + date + '/京东')
    fpath = fpath + date + '/京东/'
    for i in range(len(df)):
        jd(df.loc[i,'链接'],fpath,df.loc[i,'产品'])
filepath = r'E:\01复硕正态\08项目\08商品详情介绍图片/'
if __name__ == '__main__':
    spider_jd(filepath,'2018-4-2','京东-沐浴露产品链接.xlsx')