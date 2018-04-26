from selenium import webdriver
import time
import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

df = pd.read_excel('./采集关键词.xlsx')
url = 'http://zhishu.sogou.com/'

def spider_index_year():
    options = Options()
    browser = webdriver.Chrome(chrome_options=options.add_argument("--headless"))
    #browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    time.sleep(random.randint(2,4))
    word = '舒肤佳'
    browser.find_element_by_xpath('//*[@id="wrap"]/div/div[3]/span[1]/input[1]').clear()
    browser.find_element_by_xpath('//*[@id="wrap"]/div/div[3]/span[1]/input[1]').send_keys(word)
    js2 = "var q=document.getElementById('searchButton').click()"
    browser.execute_script(js2)
    for keyword in df['关键字'].values:
        path = './2016-2017/'
        #js3 = "var q=document.getElementById('labInput').clear()"
        # js4 = "var q=document.getElementById('labInput').clear()"
        # browser.execute_script(js3)
        browser.find_element_by_xpath('//*[@id="labInput"]').clear()
        browser.find_element_by_xpath('//*[@id="labInput"]').send_keys(keyword)
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/a').click()
        time.sleep(random.randint(2, 4))
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]')))
            browser.maximize_window()
            if not os.path.exists(path+keyword):
                os.mkdir(path+keyword)
            path = path+keyword
            if not os.path.exists(path+'/whole'):
                os.mkdir(path+'/whole')
            if not os.path.exists(path+'/pc'):
                os.mkdir(path+'/pc')
            if not os.path.exists(path+'/mobile'):
                os.mkdir(path+'/mobile')
            if not os.path.exists(path+'/whole_值'):
                os.mkdir(path+'/whole_值')
            if not os.path.exists(path+'/pc_值'):
                os.mkdir(path+'/pc_值')
            if not os.path.exists(path+'/mobile_值'):
                os.mkdir(path+'/mobile_值')
            f = open(path+'/baidu_index.txt', 'a', encoding='utf-8')

            for i in range(1,3):
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[4]').click()
                time.sleep(random.randint(1, 4))
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span[2]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/ul/li['+str(i)+']').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span[3]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/span[2]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/ul/li['+str(i)+']').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/span[3]').click()
                browser.find_element_by_xpath( '//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]/ul/li[6]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]').click()
                time.sleep(random.randint(1, 4))
                js1 = "var q=document.documentElement.scrollTop=10000"
                browser.execute_script(js1)
                time.sleep(random.randint(1,4))
                if os.path.isfile(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) +'-1'+ ".png"):
                    os.remove(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) +'-1'+ ".png")
                browser.save_screenshot(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) +'-1'+ ".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_wholeTrence_' + str(i) +'-1'+ ".png" + '\n')
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]').click()
                time.sleep(random.randint(1, 4))
                if os.path.isfile(path + r'\pc/' + keyword + '_pcTrence_' + str(i) +'-1'+ ".png"):
                    os.remove(path + r'\pc/' + keyword + '_pcTrence_' + str(i) +'-1'+ ".png")
                browser.save_screenshot(path + r'\pc/' + keyword + '_pcTrence_' + str(i) + '-1'+".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_pcTrence_' + str(i) +'-1'+ ".png" + '\n')
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[3]/div[2]/div[3]/div[1]').click()
                time.sleep(random.randint(1, 4))
                if os.path.isfile(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) +'-1'+ ".png"):
                    os.remove(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) +'-1'+".png")
                browser.save_screenshot(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) + '-1'+".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_mobileTrence_' + str(i) +'-1'+ ".png" + '\n')
                js2 = "var q=document.documentElement.scrollTop=0"
                browser.execute_script(js2)

                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[4]').click()
                time.sleep(random.randint(1, 4))
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span[3]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[7]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/span[3]').click()
                browser.find_element_by_xpath( '//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]/ul/li[12]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]').click()
                js1 = "var q=document.documentElement.scrollTop=10000"
                browser.execute_script(js1)
                time.sleep(random.randint(1,4))
                if os.path.isfile(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) +'-2'+ ".png"):
                    os.remove(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) +'-2'+ ".png")
                browser.save_screenshot(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) +'-2'+ ".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_wholeTrence_' + str(i) +'-2'+ ".png" + '\n')
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]').click()
                time.sleep(random.randint(1, 4))
                if os.path.isfile(path + r'\pc/' + keyword + '_pcTrence_' + str(i) +'-2'+ ".png"):
                    os.remove(path + r'\pc/' + keyword + '_pcTrence_' + str(i) +'-2'+ ".png")
                browser.save_screenshot(path + r'\pc/' + keyword + '_pcTrence_' + str(i) + '-2'+".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_pcTrence_' + str(i) +'-2'+ ".png" + '\n')
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[3]/div[2]/div[3]/div[1]').click()
                time.sleep(random.randint(1, 4))
                if os.path.isfile(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) +'-2'+ ".png"):
                    os.remove(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) +'-2'+".png")
                browser.save_screenshot(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) + '-2'+".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_mobileTrence_' + str(i) +'-2'+ ".png" + '\n')
                js2 = "var q=document.documentElement.scrollTop=0"
                browser.execute_script(js2)
            f.close()
        except Exception as e:
            dff.write(keyword+'\n')
            print(e)
        print(keyword)
    dff.close()
    browser.close()

def spider_index_month():
    options = Options()
    browser = webdriver.Chrome(chrome_options=options.add_argument("--headless"))
    #browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    time.sleep(random.randint(2,4))
    word = '舒肤佳'
    browser.find_element_by_xpath('//*[@id="wrap"]/div/div[3]/span[1]/input[1]').clear()
    browser.find_element_by_xpath('//*[@id="wrap"]/div/div[3]/span[1]/input[1]').send_keys(word)
    js2 = "var q=document.getElementById('searchButton').click()"
    browser.execute_script(js2)
    for keyword in df['关键字'].values:
        path = './2018/'
        #js3 = "var q=document.getElementById('labInput').clear()"
        # js4 = "var q=document.getElementById('labInput').clear()"
        # browser.execute_script(js3)
        browser.find_element_by_xpath('//*[@id="labInput"]').clear()
        browser.find_element_by_xpath('//*[@id="labInput"]').send_keys(keyword)
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/a').click()
        time.sleep(random.randint(2, 4))
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]')))
            browser.maximize_window()
            if not os.path.exists(path+keyword):
                os.mkdir(path+keyword)
            path = path+keyword
            if not os.path.exists(path+'/whole'):
                os.mkdir(path+'/whole')
            if not os.path.exists(path+'/pc'):
                os.mkdir(path+'/pc')
            if not os.path.exists(path+'/mobile'):
                os.mkdir(path+'/mobile')
            if not os.path.exists(path+'/whole_值'):
                os.mkdir(path+'/whole_值')
            if not os.path.exists(path+'/pc_值'):
                os.mkdir(path+'/pc_值')
            if not os.path.exists(path+'/mobile_值'):
                os.mkdir(path+'/mobile_值')
            f = open(path+'/baidu_index.txt', 'a', encoding='utf-8')
            for i in range(1,2):
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[4]').click()
                time.sleep(random.randint(1, 4))
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span[2]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/ul/li[3]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span[3]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]').click()#每次修改li确定抓取月份
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/span[2]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/ul/li[3]').click()
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/span[3]').click()
                browser.find_element_by_xpath( '//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]/ul/li[3]').click()#每次修改li确定抓取月份
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]').click()
                time.sleep(random.randint(1, 4))
                js1 = "var q=document.documentElement.scrollTop=10000"
                browser.execute_script(js1)
                time.sleep(random.randint(1,4))
                if os.path.isfile(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) + ".png"):
                    os.remove(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) + ".png")
                browser.save_screenshot(path + r'\whole/' + keyword + '_wholeTrence_' + str(i) + ".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_wholeTrence_' + str(i) + ".png" + '\n')
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]').click()
                time.sleep(random.randint(1, 4))
                if os.path.isfile(path + r'\pc/' + keyword + '_pcTrence_' + str(i) + ".png"):
                    os.remove(path + r'\pc/' + keyword + '_pcTrence_' + str(i) + ".png")
                browser.save_screenshot(path + r'\pc/' + keyword + '_pcTrence_' + str(i) + ".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_pcTrence_' + str(i) + ".png" + '\n')
                browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[3]/div[2]/div[3]/div[1]').click()
                time.sleep(random.randint(1, 4))
                if os.path.isfile(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) + ".png"):
                    os.remove(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) + ".png")
                browser.save_screenshot(path + r'\mobile/' + keyword + '_mobileTrence_' + str(i) + ".png")
                f.write(str(2015 + i) + '：' + '  ' + keyword + '_mobileTrence_' + str(i) + ".png" + '\n')
                js2 = "var q=document.documentElement.scrollTop=0"
                browser.execute_script(js2)
            f.close()
            time.sleep(random.randint(2,6))
        except Exception as e:
            dff.write(keyword+'\n')
            print(e)
        print(keyword)
    dff.close()
    browser.close()
dff = open('./2016-2017/无效关键词.txt','a',encoding='utf-8')
#dff = open('./2018/无效关键词.txt','a',encoding='utf-8')
if __name__ == '__main__':
    spider_index_year()
    #spider_index_month()




