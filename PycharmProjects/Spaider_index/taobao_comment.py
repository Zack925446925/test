# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
from bs4 import BeautifulSoup


browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

# 模拟页面搜索
def search_goods():
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.clear()
        input.send_keys('沐浴露')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        #        print(total.text)
        return total.text
    except Exception as e:
        print(e)


# 模拟翻页及获取单页商品的url
def next_page(page_number):
    try:
        urls1 = []
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, \
                                                     '#mainsrp-pager > div > div > div > ul > li.item.active > span'),
                                                    str(page_number)))

        html = browser.page_source
        #    print(html)
        soup = BeautifulSoup(html, 'lxml')
        #    print(soup)
        urls = soup.select('.m-itemlist .J_MouserOnverReq .title .J_ClickStat')
        #    for u in urls:
        #        print(type(u['href']))
        #    print(urls)
        for i in urls:
            if re.search('^http', i['href']):
                with open('C:/Users/tange/Desktop/测试数据/taobao_goods_urls', 'a+') as f:
                    f.write(i['href'].strip() + '\n')
                    f.flush()
            else:
                with open('C:/Users/tange/Desktop/测试数据/taobao_goods_urls', 'a+') as f:
                    f.write('https' + i['href'].strip() + '\n')
                    f.flush()
            urls1.append(str(i['href']).strip())
            print(str(i['href']).strip())
    except Exception as e:
        print(e)
    return urls1


# 读取商品的url
def read_goods_url(filepath):
    with open(filepath, 'r') as f:
        goods_urls = f.readlines()
        return goods_urls


# 获取商品评论的url
def get_comment_url(url):
    html = ''
    res = ''
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
        res = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
    soup = BeautifulSoup(res.text, 'lxml')
    try:
        if re.search('tmall', url):
            tm_part1 = 'https://rate.tmall.com/list_detail_rate.htm?itemId='
            tm_part2 = '&spuId='
            tm_part3 = '&sellerId='
            tm_part4 = '&order=3&currentPage=1'
            tm_pattern1 = re.compile('itemId=(\d+)', re.S)
            itemId = re.findall(tm_pattern1, str(soup))[0]
            #    print(itemId)
            tm_pattern2 = re.compile('sellerId=(\d+)', re.S)
            sellerId = re.findall(tm_pattern2, str(soup))[0]
            #    print(sellerId)
            tm_pattern3 = re.compile('spuId=(\d+)', re.S)
            spuId = re.findall(tm_pattern3, str(soup))[0]
            #    print(spuId)
            html = tm_part1 + itemId + tm_part2 + spuId + tm_part3 + sellerId + tm_part4
            #        print(html)
        elif re.search('taobao', url):
            tb_part1 = 'https://rate.taobao.com/feedRateList.htm?auctionNumId='
            tb_part2 = '&userNumId='
            tb_part3 = '&currentPageNum=1'
            tb_pattern1 = re.compile('auctionNumId=(\d+)', re.S)
            auctionNumId = re.findall(tb_pattern1, str(soup))[0]
            tb_pattern2 = re.compile('userId=(\d+)', re.S)
            userNumId = re.findall(tb_pattern2, str(soup))[0]
            html = tb_part1 + auctionNumId + tb_part2 + userNumId + tb_part3

        else:
            print('url不符合要求')
        with open('C:/Users/tange/Desktop/测试数据/taobao_comment_url', 'a+') as f:
            f.write(html + '\n')
            f.flush()
            #        print(html)
    except Exception as e:
        print(e)
    return html


# 获取1-100页的商品评论链接
def get_more_comment_url(filepath):
    with open(filepath, 'r') as f:
        df = f.readlines()
    for i in df:
        if re.search('currentPageNum=', i, re.S):
            part1 = i.split('currentPageNum=')[0]
            part2 = 'currentPageNum='
            for j in range(1, 100):
                url = part1 + part2 + str(j)
                with open('C:/Users/tange/Desktop/测试数据/taobao_100_comment', 'a+') as f1:
                    f1.write(url + '\n')
                    f1.flush()
        else:
            part1 = i.split('currentPage=')[0]
            part2 = 'currentPage='
            for j in range(1, 100):
                url = part1 + part2 + str(j)
                with open('C:/Users/tange/Desktop/测试数据/taobao_100_comment', 'a+') as f1:
                    f1.write(url + '\n')
                    f1.flush()


# 主函数
def main():
    total = search_goods()
    print(total)
    pattern = re.compile('(\d+)',re.S)
    total = int(re.search(pattern,total).group(1))
    print(total)
    for i in range(1,total+1):
        next_page(i)
    '''filepath = 'C:/Users/tange/Desktop/测试数据/taobao_goods_urls'
    goods_url = read_goods_url(filepath)
    for i in goods_url:
        urls = get_comment_url(i)
    filepath1 = 'C:/Users/tange/Desktop/测试数据/taobao_comment_url'
    get_more_comment_url(filepath1)'''


if __name__ == '__main__':
    main()





