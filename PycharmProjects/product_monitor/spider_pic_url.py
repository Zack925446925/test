import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import  random
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''filepath1 = r'E:/01复硕正态/08项目/01沐浴露监测/01测试数据/01旗舰店数据/2017-12-28王/'
filepath2 = r'E:/01复硕正态/08项目/01沐浴露监测/02成品数据/旗舰店数据/2017-12-28王/'''
filepath1 = r'E:\01复硕正态\08项目\04中华项目监测\01测试数据/01旗舰店数据\2017-12-28王/'
filepath2 = r'E:\01复硕正态\08项目\04中华项目监测\02成品数据/旗舰店数据\2017-12-28王/'
#获取文件名
def get_filename(path):
    filename = os.listdir(path)
    return filename

def func_jd(url):
    # df['产品链接'].head()
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    headers = {'User-Agent':'Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 59.0) Gecko / 20100101Firefox / 59.0'}
    # ip, port = ("58.19.14.182", "18118")
    # proxy_url = "http://{0}:{1}".format(ip, port)
    # proxy_dict = {
    #     "http": proxy_url
    # }proxies=proxy_dict,
    # browser = webdriver.Ie(url)
    html = []
    title = []
    html_pic = []
    #res = browser.page_source
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    pat = re.compile('(.*?)\d+(.*?)', re.S)
    part1 = re.search(pat, url).group(1)
    # part2 = re.search(pat,url).group(2)
    # print(part2)

    if soup.select('#choose-attrs .dd .item'):
        bianhao = soup.select('#choose-attrs .dd .item')
        bh = []
        for i in bianhao:
            bh.append(i['data-sku'])
        for j in range(len(bh)):
            html.append(part1 + str(bh[j]) + '.html')
        html = list(set(html))
        for u in html:
            # for k in u:
            print(u)
            #browser1 = webdriver.PhantomJS(u)
            #res1 = browser1.page_source
            res1 = requests.get(u, headers=headers)
            soup1 = BeautifulSoup(res1.text, 'lxml')
            title1 = soup1.select('.w .itemInfo-wrap .sku-name')[0].text.strip()
            title.append(title1)
            html_pic1 = soup1.select('#spec-list li img')[0]['src']
            html_pic.append('https:' + html_pic1)
            #browser1.close()
    else:
        title.append(soup.select('.w .itemInfo-wrap .sku-name')[0].text.strip())
        html.append(url)
        html_pic.append('https:' + soup.select('#spec-list li img')[0]['src'])

    data = pd.DataFrame({'产品': title, '链接': html, '图片链接': html_pic})
    #browser.close()
    return data

def spider_pic_url(filepath1):
    filename = get_filename(filepath1)
    for name in filename:
        df = pd.read_excel(filepath1 + name)
        writer = pd.ExcelWriter(filepath2+name)
        data0 = pd.DataFrame(columns=['产品' , '链接', '图片链接'])
        for i in df.loc[:,'链接']:
            data = func_jd(i)
            data0 = pd.concat([data0, data])
        #print(data0)
        data0.to_excel(writer,index=False)
        writer.save()
def spider_first_jd(url,path,name):
    #browser = webdriver.Chrome()
    browser = webdriver.Firefox()
    #browser = webdriver.PhantomJS()
    browser.get(url)
    res = browser.page_source
    soup = BeautifulSoup(res, 'lxml')
    #print(soup)
    #print('--------------------------------------------')
    url = []
    title = []
    pic_url = []

    for tag in soup.select('.j-module .jSubObject'):
        #print(tag)
        #print('-----------------')
        pic_url.append('https:' + tag.select('.jPic a img')[0]['src'])
        url.append('https:' + tag.select('.jGoodsInfo .jDesc a')[0]['href'])
        title.append(tag.select('.jGoodsInfo .jDesc a')[0].text.strip())
        #print(tag.select('.jPic a img')[0]['src'],'/////////',tag.select('.jGoodsInfo .jDesc a')[0]['href'],'/////////',tag.select('.jGoodsInfo .jDesc a')[0].text.strip())
    df = pd.DataFrame({'产品':title, '链接':url, '图片链接':pic_url})
    data0 = pd.DataFrame(columns=['产品', '链接', '图片链接'])
    for i in df.loc[:, '链接']:
        print(i)
        data = func_jd(i)
        data0 = pd.concat([data0, data])
    data0 = data0.reset_index(drop=True)
    if os.path.isfile(path+'京东/'+name+'.xls'):
        os.remove(path+'京东/'+name+'.xls')
    data0.to_excel(path + '京东/' +  name + '.xls', index=False)
    print(name)
    #data0.to_excel(filepath2 + '强生.xls')

def spider_first_tm(url,path,name):
    browser = webdriver.Chrome()
    #browser = webdriver.PhantomJS()
    browser.get(url)
    browser.maximize_window()
    time.sleep(random.randint(3,7))
    '''if browser.find_element_by_id("TPL_username_1"):
        browser.find_element_by_id("TPL_username_1").clear()
        browser.find_element_by_id("TPL_password_1").clear()
        account = []
        try:
            fileaccount = open(r"E:\01复硕正态\01数据爬取\06指数抓取\01百度指数/account1.txt")
            accounts = fileaccount.readlines()
            for acc in accounts:
                account.append(acc.strip())
            fileaccount.close()
        except Exception as err:
            print(err)
            input("请正确在account.txt里面写入账号密码")
            exit()
        browser.find_element_by_id("TPL_username_1").send_keys(account[0])
        browser.find_element_by_id("TPL_password_1").send_keys(account[1])
        browser.find_element_by_id("J_SubmitStatic").click()'''
    handles = browser.window_handles
    browser.switch_to_window(handles[-1])
    #print(browser.find_element_by_id('J_sufei'))
    if is_element_exist_id(browser, 'J_sufei'):#browser.find_element_by_id("TANGRAM_12__userName"):
        time.sleep(random.randint(1, 3))
        browser.refresh()
        # account = []
        # print(account)
        # browser.switch_to.frame(0)
        # try:
        #     fileaccount = open(r"E:\01复硕正态\07数据清洗/account1.txt")
        #     accounts = fileaccount.readlines()
        #     for acc in accounts:
        #         account.append(acc.strip())
        #     fileaccount.close()
        #     print(account)
        # except Exception as err:
        #     print(err)
        #     input("请正确在account1.txt里面写入账号密码")
        #     exit()
        #
        # browser.find_element_by_xpath('//*[@id="TPL_username_1"]').clear()
        # browser.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys(account[0])
        # browser.find_element_by_xpath('//*[@id="TPL_password_1"]').clear()
        # browser.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys(account[1])
        # time.sleep(2)
        # browser.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
        # time.sleep(2)
        # browser.switch_to_default_content()
    wait = WebDriverWait(browser, 10)
    total = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ShopSearchResult > div > div.filter.clearfix.J_TFilter > p > b.ui-page-s-len')))
    num = total.text.strip().split('/')
    print(num)
    url = []
    title = []
    pic_url = []
    for d  in range(int(num[1])):
        # js = "var q=document.body.scrollHeight ;return(q)"
        # Text_height = browser.execute_script(js)
        # n = Text_height // 500
        # print(n)
        # for i in range(int(n)):
        #     js = "var q=document.documentElement.scrollTop=" + str((i + 1) * 500)
        #     browser.execute_script(js)
        #     time.sleep(1)
        #
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
        #print(soup.select('#J_ShopSearchResult .skin-box-bd .J_TItems'))
        item = list(soup.select('#J_ShopSearchResult .skin-box-bd .J_TItems')[0].children)
        item_new = []
        if item[1]['class'][0] == 'item5line1':
            for index, value in enumerate(item):
                if not isinstance(value, str):
                    #print(value['class'][0])
                    if value['class'][0] != 'item5line1':
                        break
                    else:
                        item_new.append(value)
        elif item[1]['class'][0] == 'item4line1':
            for index, value in enumerate(item):
                if not isinstance(value, str):
                    #print(value['class'][0])
                    if value['class'][0] != 'item4line1':
                        break
                    else:
                        item_new.append(value)

        for i in item_new:
            for j in i.select('.item'):
                pic_url.append('https:' + j.select('.photo img')[0]['src'])
                url.append('https:' + j.select('.detail a')[0]['href'])
                title.append(j.select('.detail a')[0].text.strip())
        js1 = "var q=document.documentElement.scrollTop=0"
        browser.execute_script(js1)
        num1 = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ShopSearchResult > div > div.filter.clearfix.J_TFilter > p > b.ui-page-s-len'))).text.strip().split('/')[0]
        print(num1,num[1])
        if num1 != num[1]:
            submit = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#J_ShopSearchResult > div > div.filter.clearfix.J_TFilter > p > a')))
            submit.click()
    df = pd.DataFrame({'产品':title, '链接': url, '图片链接':pic_url})
    if os.path.isfile(path+'天猫/'+name+'.xls'):
        os.remove(path+'天猫/'+name+'.xls')
    df.to_excel(path+'天猫/'+name+'.xls',index=False)
    print('成功抓取：' + name + '.xls')

def is_element_exist(drive,s):
    flag = True
    try:
        if drive.find_element_by_xpath(s):
            return flag
    except Exception as e:
        flag = False
        return flag
def is_element_exist_id(drive,s):
    flag = True
    try:
        if drive.find_element_by_id(s):
            return flag
    except Exception as e:
        flag = False
        return flag

def spider_first(path):
    df1 = pd.read_excel(path+'品牌链接.xls')
    for i in range(len(df1)):
        if df1.iloc[i,0] == '天猫':
            spider_first_tm(df1.iloc[i,1],path,df1.iloc[i,2])
        elif df1.iloc[i,0] == '京东':
            spider_first_jd(df1.iloc[i, 1], path, df1.iloc[i, 2])

filepath = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\店铺商品链接/'
#filepath = r'E:\01复硕正态\08项目\04中华项目监测\02成品数据\旗舰店数据\店铺商品链接/'
def main():
    #spider_pic_url(filepath1)
    spider_first(filepath)


if __name__ == '__main__':
    main()