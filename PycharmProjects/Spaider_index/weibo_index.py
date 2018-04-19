import requests
import time
import os
import pandas as pd
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Accept':'*/*',

}
res = requests.get('http://data.weibo.com/index/ajax/getchartdata?month=default&__rnd=1520831579162',headers = headers)
print(type(res.text))
