import os
import hashlib
import logging
import sys
import pandas as pd
from PIL import Image
def logger(name):
    """ 获取logger"""
    logger = logging.getLogger()
    if not logger.handlers:
        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        # 文件日志
        file_handler = logging.FileHandler(r'C:\Users\tange\PycharmProjects\product_monitor\pic_log/'+ name+ '.log')
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值
        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(logging.INFO)
    return logger
def get_md5(filename):
    m = hashlib.md5()
    mfile = open(filename, "rb")
    m.update(mfile.read())
    mfile.close()
    md5_value = m.hexdigest()
    return md5_value


def get_urllist(path):
    # 替换指定的文件夹路径即可
    base = (path)
    list = os.listdir(base)
    urlList = []
    for i in list:
        url = base + i
        urlList.append(url)
    return urlList
def getCode(img, size=(9, 8)):
    result = []
    # print("x==",size[0])
    # print("y==",size[1]-1)
    img = img.resize(size).convert('L')
    x_size = size[0] - 1  # width
    y_size = size[1]  # high
    for x in range(0, x_size):
        for y in range(0, y_size):
            now_value = img.getpixel((x, y))
            next_value = img.getpixel((x + 1, y))

            if next_value < now_value:
                result.append(1)
            else:
                result.append(0)

    return str(result)


def compCode(code1, code2):
    num = 0
    for index in range(0, len(code1)):
        if code1[index] != code2[index]:
            num += 1
    return num


def classfiy_dHash(image1, image2, size=(9, 8)):
    ''' 'image1' and 'image2' is a Image Object.
    You can build it by 'Image.open(path)'.
    'Size' is parameter what the image will resize to it and then image will be compared to another image by the dHash.
    It's 9 * 8 when it default.
    The function will return the hamming code,less is correct.
    '''
    image1 = image1.resize(size).convert('L')
    code1 = getCode(image1, size)

    image2 = image2.resize(size).convert('L')
    code2 = getCode(image2, size)

    assert len(code1) == len(code2), "error"
    #print('hello')
    return compCode(code1, code2)
def pic_repetition(path):
    for name1 in ['天猫/', '京东/']:
        for name in os.listdir(path + name1):
            log = logger(name)
            md5List = []
            urlList = get_urllist(path+ name1 +  name + '/')
            for a in urlList:
                md5 = get_md5(a)
                if (md5 in md5List):
                    os.remove(a)
                    log.info("重复：%s" % a)
                else:
                    md5List.append(md5)
                    # print(md5List)
            print("一共%s张照片" % len(md5List))
def pic_repetition1(path):
    for name1 in ['天猫/', '京东/']:
        for name in os.listdir(path + name1):

            #log = logger(name)
            code_List = []
            urlList = get_urllist(path+ name1 +  name + '/')
            for a in urlList:
                im = Image.open(a)
                pic_code = getCode(im,size=(9, 8))
                if (pic_code in code_List):
                    os.remove(a)
                    #log.info("重复：%s" % a)
                else:
                    code_List.append(pic_code)
                    # print(md5List)
            print("一共%s张照片" % len(code_List))
            urlList1 = get_urllist(path + name1 + name + '/')
            srcdir = path + name1 + name + '/'
            index = 1
            for srcfile in urlList1:
                sufix = os.path.splitext(srcfile)[1]
                destfile = srcdir + "//(" + u"%d" % (index) + ')' + sufix
                srcfile = os.path.join(srcdir, srcfile)
                os.rename(srcfile, destfile)
                index += 1


# fpath1 = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\新链接判断图库/'
# fpath2 = r'E:\A_judge_pic\2017-11-15/'
# fpath3 = r'E:\01复硕正态\08项目\01沐浴露监测\02成品数据\旗舰店数据\2018-3-31/'

fpath1 = r'G:\01复硕正态\08项目\04中华项目监测\02成品数据\旗舰店数据\新链接判断图片/'
fpath2 = r'G:\A_judge_pic\toothpaste/'
fpath3 = r'G:\01复硕正态\08项目\04中华项目监测\02成品数据\旗舰店数据\2018-4-13/'

def judge_new_url_pic(filepath1, filepath2 ,filepath3):
    word = ['天猫/', '京东/']
    for name1 in word:
        for name2 in os.listdir(filepath1 + name1):
            df = pd.read_excel(filepath3 + name1 + '不同链接数据提取'  + '/' +  name2 + '.xls')
            md5List = {}
            urlList = get_urllist(filepath1 + name1 + '/' + name2 +'/')
            for a in urlList:
                im = Image.open(a)
                md5List[getCode(im)] = a
            print(md5List)
            #print(md5List)
            for i in range(len(df)):
                im1 = Image.open(filepath2 + df.loc[i,'图片链接'])
                md5 = getCode(im1)
                print(md5)
                if md5 in md5List:
                    print(md5List[md5],md5)
                    print('****************')
                    df.loc[i,'旧图片名称'] = md5List[md5]
            if os.path.isfile(filepath3 + name1 + '不同链接数据提取' + '/' + name2 + '.xls'):
                os.remove(filepath3 + name1 + '不同链接数据提取' + '/' + name2 + '.xls')
            df.to_excel(filepath3 + name1 + '不同链接数据提取' + '/' + name2 + '.xls',index=False)

if __name__ == '__main__':
    judge_new_url_pic(fpath1,fpath2,fpath3)
    #pic_repetition1(fpath1)