from selenium import webdriver
import time
import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
url = 'https://trends.so.com/'

def is_element_exist_class_name(drive, s):
    flag = True
    try:
        if drive.find_element_by_class_name(s).is_displayed():
            return flag
    except Exception as e:
        flag = False
        return flag

def login():
    #browser = webdriver.Chrome()
    browser = webdriver.PhantomJS()
    browser.get(url)
    browser.maximize_window()
    time.sleep(2)
    wait = WebDriverWait(browser,10)
    account = []
    with open(fpath1+'account.txt') as f:
        accounts = f.readlines()
        for line in accounts:
            account.append(line.strip())
    input1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#index > header > div > ul > li:nth-child(1) > a')))
    input1.click()
    input3 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'quc-input-account')))
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.quc-panel.quc-wrapper > div.quc-panel-bd > div > div.quc-main > form > p.quc-field.quc-field-submit > input')))
    input3.clear()
    input3.send_keys(account[0])
    browser.find_element_by_class_name('quc-input-password').clear()
    browser.find_element_by_class_name('quc-input-password').send_keys(account[1])
    if is_element_exist_class_name(browser,'quc-input-captcha'):
        captcha = input('请输入验证码：')
        browser.find_element_by_class_name('quc-input-captcha').clear()
        browser.find_element_by_class_name('quc-input-captcha').send_keys(captcha)
    submit.click()
    time.sleep(random.randint(4,7))
    keyword = '男士洁面'
    browser.find_element_by_xpath('//*[@id="index"]/div[1]/form/input').clear()
    browser.find_element_by_xpath('//*[@id="index"]/div[1]/form/input').send_keys(keyword)
    browser.find_element_by_xpath('//*[@id="index"]/div[1]/form/button').click()
    time.sleep(random.randint(3, 5))
    return browser,wait
def spider_index_year(browser,wait):
    df = pd.read_excel(fpath1+'/采集关键词.xlsx')
    # if os.path.isfile(filepath+'/无效关键词.xlsx'):
    #     os.remove(filepath+'/无效关键词.xlsx')
    fff = open(filepath+'/无效关键词.xlsx','a',encoding='utf-8')
    for value in df['关键字'].values:
        try:
            input2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#header > div.wrap.clearfix > div.search > form > input[type="text"]')))
            input2.clear()
            input2.send_keys(value)
            browser.find_element_by_css_selector('#header > div.wrap.clearfix > div.search > form > button').click()
            time.sleep(2)
            element1 = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#trend_wrap > svg > g:nth-child(5) > g:nth-child(4) > text:nth-child(2)')))
            if not os.path.exists(filepath + value):
                os.mkdir(filepath + value)
            if not os.path.exists(filepath+value+'/whole'):
                os.mkdir(filepath+value+'/whole')
            # if not os.path.exists(filepath+value+'/pc'):
            # 	os.mkdir(filepath+value+'/pc')
            # if not os.path.exists(filepath+value+'/mobile'):
            # 	os.mkdir(filepath+value+'/mobile')
            if not os.path.exists(filepath+value+'/whole_值'):
                os.mkdir(filepath+value+'/whole_值')
            # if not os.path.exists(filepath+value+'/pc_值'):
            # 	os.mkdir(filepath+value+'/pc_值')
            # if not os.path.exists(filepath+value+'/mobile_值'):
            # 	os.mkdir(filepath+value+'/mobile_值')
            if os.path.isfile(filepath+value+'/baidu_index.txt'):
                os.remove(filepath+value+'/baidu_index.txt')
            ff = open(filepath + value + '/baidu_index.txt', 'a', encoding='utf-8')

            for i in range(5):
                element = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#trend_wrap > svg > g:nth-child(5) > g:nth-child(4) > text:nth-child(2) > tspan')))
                if element:
                    ActionChains(browser).move_to_element(element).perform()
                elif element1:
                    ActionChains(browser).move_to_element(element1).perform()
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[1]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[1]/option[' + str(i+1) + ']').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[2]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[2]/option[1]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[1]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[1]/option[' + str(i+1)+']').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[2]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[2]/option[6]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/p/button[1]').click()
                time.sleep(3)
                if os.path.isfile(filepath +  value + '/whole/'+ value+'_wholeTrence_' + str(i) + '-1' + ".png"):
                    os.remove(filepath +  value + '/whole/'+ value+'_wholeTrence_' + str(i) +'-1' + ".png")
                browser.save_screenshot(filepath +  value + '/whole/'+ value+'_wholeTrence_' + str(i) + '-1' +".png")
                ff.write(str(2013 + i) + '：' + '  ' + value + '_wholeTrence_' + str(i) + '-1' +".png" + '\n')
                element = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#trend_wrap > svg > g:nth-child(5) > g:nth-child(4) > text:nth-child(2) > tspan')))
                # browser.refresh()
                # time.sleep(3)
                element2 = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR,'#trend_wrap > svg > g:nth-child(5) > g:nth-child(4) > g:nth-child(8) > text > tspan')))
                ActionChains(browser).move_to_element(element2).perform()
                ActionChains(browser).move_to_element(element).perform()
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[2]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[2]/option[7]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[2]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[2]/option[12]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/p/button[1]').click()
                time.sleep(3)
                if os.path.isfile(filepath +  value + '/whole/'+ value+'_wholeTrence_' + str(i) + '-2' + ".png"):
                    os.remove(filepath +  value + '/whole/'+ value+'_wholeTrence_' + str(i) +'-2' + ".png")
                browser.save_screenshot(filepath +  value + '/whole/'+ value+'_wholeTrence_' + str(i) + '-2' +".png")
                ff.write(str(2013 + i) + '：' + '  ' + value + '_wholeTrence_' + str(i) + '-2' +".png" + '\n')
            ff.close()
            time.sleep(random.randint(2,6))
        except Exception as e:
            fff.write(value+'\n')
            print(e)
        print(value)
    fff.close()
    #browser.close()
def spider_index_month(browser,wait):
    df = pd.read_excel(fpath1+'/采集关键词.xlsx')
    if os.path.isfile(filepath+'/无效关键词.xlsx'):
        os.remove(filepath+'/无效关键词.xlsx')
    fff = open(filepath+'/无效关键词.txt','a',encoding='utf-8')
    for value in df['关键字'].values:
        try:
            input2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#header > div.wrap.clearfix > div.search > form > input[type="text"]')))
            input2.clear()
            input2.send_keys(value)
            browser.find_element_by_css_selector('#header > div.wrap.clearfix > div.search > form > button').click()
            time.sleep(2)
           
            element = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#trend_wrap > svg > g:nth-child(5) > g:nth-child(4) > text:nth-child(2)')))
            if not os.path.exists(filepath + value):
                os.mkdir(filepath + value)
            if not os.path.exists(filepath+value+'/whole'):
                os.mkdir(filepath+value+'/whole')
            if not os.path.exists(filepath+value+'/whole_值'):
                os.mkdir(filepath+value+'/whole_值')
            if os.path.isfile(filepath+value+'/baidu_index.txt'):
                os.remove(filepath+value+'/baidu_index.txt')
            ff = open(filepath + value + '/baidu_index.txt', 'a', encoding='utf-8')
            for i in range(1,2):
                element = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#trend_wrap > svg > g:nth-child(5) > g:nth-child(4) > text:nth-child(2)')))
                ActionChains(browser).move_to_element(element).perform()
                time.sleep(random.randint(1,2))
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[1]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[1]/option[6]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[2]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[1]/dd/select[2]/option[3]').click()#每次修改这里的option确定抓取月份
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[1]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[1]/option[6]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[2]').click()
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/dl[2]/dd/select[2]/option[3]').click()#每次修改这里的option确定抓取月份
                browser.find_element_by_xpath('//*[@id="trend_wrap"]/div[2]/p/button[1]').click()
                time.sleep(3)
                if os.path.isfile(filepath +  value + 'whole/'+ value+'_wholeTrence_' + str(i) + ".png"):
                    os.remove(filepath +  value + 'whole/'+ value+'_wholeTrence_' + str(i) + ".png")
                browser.save_screenshot(filepath +  value + 'whole/'+ value+'_wholeTrence_' + str(i) + ".png")
                ff.write(str(2013 + i) + '：' + '  ' + value + '_wholeTrence_' + str(i) + ".png" + '\n')
            ff.close()
            time.sleep(random.randint(2,6))
        except Exception as e:
            fff.write(value+'\n')
            print(e)
        print(value)
    fff.close()
    browser.close()
fpath1 = './'
filepath = './2013-2017/'
#filepath = './2018/'
if __name__ == '__main__':
    driver,wait = login()
    spider_index_year(driver,wait)
    spider_index_month(driver, wait)