from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
url = 'https://www.jd.com/'
browser.get(url)
time.sleep(2)
input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="key"]')))
submit = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]/div/div[2]/button')))
input.clear()
input.send_keys('沐浴露')
submit.click()
time.sleep(2)
browser.maximize_window()
browser.find_element_by_xpath('//*[@id="J_filter"]/div[1]/div[1]/a[2]/span').click()
time.sleep(2)
total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_topPage > span > i')))
#page_num = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_topPage > span > b')))
url = []
title = []
number = 0
for i in range(int(total.text)):
    res = browser.page_source
    soup = BeautifulSoup(res, 'lxml')
    for tag in soup.select('.gl-warp .gl-item'):
        title1 = tag.select('.p-name em')[0].text
        if '+' not in title1:
            url.append('https:' + tag.select('.p-name a')[0]['href'])
            title.append(title1)
            number += 1
            print(number)
        elif '+' not in title1:
            url.append('https:' + tag.select('.p-name a')[0]['href'])
            title.append(title1)
            number += 1
            print(number)
        elif '*' not in title1:
            url.append('https:' + tag.select('.p-name a')[0]['href'])
            title.append(title1)
            number += 1
            print(number)
    browser.find_element_by_xpath('//*[@id="J_topPage"]/a[2]').click()
    time.sleep(2)
    if number > 500:
        break
title_final = []
url_final = []
def extract_zhongwen(s):
    for i in re.findall('[\da-zA-Z-]*', s):
        if i:
            s = s.replace(i, '')
    return s
for i in range(len(title)):
    word1 = extract_zhongwen(title[i])
    if word1 not in title_final:
        title_final.append(title[i])
        url_final.append(url[i])

df = pd.DataFrame({'产品':title_final, '链接':url_final})
if os.path.isfile(r'C:\Users\tange\Desktop\测试数据/沐浴露—单品.xlsx'):
    os.remove(r'C:\Users\tange\Desktop\测试数据/沐浴露—单品.xlsx')
df.to_excel(r'C:\Users\tange\Desktop\测试数据/沐浴露—单品.xlsx',index=False)

