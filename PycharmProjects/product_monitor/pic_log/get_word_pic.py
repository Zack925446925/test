from aip import AipOcr
import os
from PIL import Image
APP_ID = '10601387'
API_KEY = 'dS2c4lwQb6O4vPGtxwaV1Ba9'
SECRET_KEY = 'GUYDc2Erq0GLsL9HBMXeVWgh9AHvl9zI'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def get_word_pic(filepath):
    demo = ''
    for pic_name in os.listdir(filepath):
        img = get_file_content(filepath + pic_name)
        text = client.webImage(img)['words_result']
        for word in text:
            demo += word['words']
        demo = demo + '\n'
        print(demo)
    with open(filepath + 'text.txt','w',encoding='utf-8') as f:
        f.write(demo)
    return demo
#fpath = r'E:\01复硕正态\07数据清洗\test\xuancheng1/'
fpath = r'C:\Users\tange\Desktop\测试数据\舒肤佳\10/'

def switch_pic(filepath):
    for name in os.listdir(filepath):
        img = Image.open(filepath + name)
        img = img.convert('L')
        img.save(filepath + 'L' + name)
if __name__ == '__main__':
    get_word_pic(fpath)
    #switch_pic(fpath)