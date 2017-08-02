# -*- coding:utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import re
import time


class GuShiWen:
    def __init__(self):

        self.User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 ' \
                          '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = {'User-Agent': self.User_Agent}

    def getPage(self, pageCount):
        try:
            # url = "http://so.gushiwen.org/type.aspx?p="+str(pageCount)+"&t=%E5%AE%8B%E8%AF%8D%E7%B2%BE%E9%80%89"
            # url = 'http://so.gushiwen.org/type.aspx?p='+str(pageCount)http://so.gushiwen.org/search.aspx?value=%E6%9D%9C%E7%94%AB
            # url = 'http://www.gushiwen.org/default_'+str(pageCount)+'.aspx'
            # url  = 'http://so.gushiwen.org/search.aspx?type=author&page='+str(pageCount)+'&value=%E6%9D%9C%E7%94%AB'
            url = "http://www.t66y.com/htm_data/16/1707/2496908.html"
            # 构建请求的request
            reqst = urllib.request.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            repse = urllib.request.urlopen(reqst)
            # 将页面转换为utf-8编码
            pageCode = repse.read().decode('utf-8')
            return pageCode
        except urllib.request.URLError as e:
            if hasattr(e, 'reason'):
                print(u'失败', e.reason)
                return None

    def start(self):
        self.getPage()



def getallpagelist(pagecode):
    soup = BeautifulSoup(pagecode, "lxml")
    soup.prettify()
    temp = soup.select('.bookcont')
    # <span><a href="/guwen/bookv_3347.aspx">第三十八章</a></span>
    pattern = re.compile('<span><a href="(.*?)</a></span>', re.S)
    items = re.findall(pattern, "".join(temp))
    print(items)


def writeTxtFile(content):
    file_object = open('杜甫.txt', 'a', encoding='utf-8')
    file_object.write(content+'\n')
    file_object.close()


def getContent(conList):
    for i in conList:
        writeTxtFile(i.string)


if __name__ == '__main__':
    reader = GuShiWen()
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    time1 = time.strftime(ISOTIMEFORMAT, time.localtime())
    print(time1)
    #循环操作
    for page in range(1, 800):
        pageCode = reader.getPage(page)
        soup = BeautifulSoup(pageCode, 'lxml')
        conList = soup.find_all('textarea')
        print(page)
        if (len(conList)> 0):
            getContent(conList)
        else:
            break
    time2 = time.strftime(ISOTIMEFORMAT, time.localtime())
    print(time2)



