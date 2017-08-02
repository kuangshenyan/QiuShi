# -*- coding:utf-8 -*-

import urllib.request
import re
from bs4 import BeautifulSoup


# 糗事百科爬虫类
class QSBK:
    # 初始化方法定义一些变量
    def __init__(self):
        self.pageIndex = 1
        # User-Agent可从浏览器中查看
        self.user_agent = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64)' \
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    # 传入某一页的页码获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/text/page/' + str(pageIndex)
            # 构建请求的request
            reqst = urllib.request.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            repse = urllib.request.urlopen(reqst)
            # 将页面转换为utf-8编码
            pageCode = repse.read().decode('utf-8')
            return pageCode
        except urllib.request.URLError as e:
            if hasattr(e, 'reason'):
                print(u'连接糗事百科失败，错误原因', e.reason)
                return None

    # # 传入某一页页码，返回本页不带图片的段子列表
    # def getPageItems(self, pageIndex):
    #     pageCode = self.getPage(pageIndex)
    #     if not pageCode:
    #         print('页面加载失败。。。。。')
    #         return None
    #     # 根据正则表达式匹配段子的内容
    #     pattern = re.compile('<div class="content">.*?<span>(.*?)</span>.*?</div>', re.S)
    #     items = re.findall(pattern, pageCode)
    #     # 用来存储每页的段子
    #     pageStories = []
    #     # 遍历正则表达式匹配的信息
    #     for item in items:
    #         # 是否含有图片
    #         haveImg = re.search('img', item)
    #         # 如果不含有图片,切文字长度大于20，把它加入list中
    #         if not haveImg and len(item) > 20:
    #             # 使用'\n'替换'<br/>'
    #             replaceBR = re.compile('<br/>')
    #             text = re.sub(replaceBR, '\n', item)
    #             pageStories.append(text.strip())
    #     return pageStories

    def getPageItemsWitHPingLun(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print('页面加载失败。。。。。')
            return None
        # 根据正则表达式匹配段子的内容
        soup = BeautifulSoup(pageCode, 'lxml')
        soup.prettify()
        duanzis = soup.find_all("div", {"class": "article block untagged mb15 typs_hot"})
        duanzis += soup.find_all("div", {"class": "article block untagged mb15 typs_long"})
        duanzis += soup.find_all("div", {"class": "article block untagged mb15 typs_old"})
        pageStories = []
        for item in duanzis:
            shenping = "【神评】"
            pattern = re.compile('<div class="content">.*?<span>(.*?)</span>.*?</div>', re.S)
            dataStr = str(item)
            # print(dataStr)
            info = re.findall(pattern, dataStr)[0].replace('<br/>', '\n').replace('\n', '')
            if "main-text" in dataStr:
                shenpingPattern = re.compile('<div class="main-text">(.*?)<div class="likenum">', re.S)
                pinglun = re.findall(shenpingPattern, dataStr)
                shenping += pinglun[0].replace('\n', '')
            else:
                shenping += "无神评论"
            # print(str(info) + '\n' + shenping)
            pageStories.append(str(info) + '\n' + shenping)
        return pageStories

    # 加载并提取页面内容，加入到列表中
    def loadPage(self):
        # 如果当前未看的页数少于2，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                # 获取新的一页
                # pageStories = self.getPageItems(self.pageIndex)
                pageStories = self.getPageItemsWitHPingLun(self.pageIndex)
                # 将该页段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完成之后页码索引加一，表示下一次读取的页码
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def getOneStroy(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            inpt = input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 如果输入Q则结束程序
            if inpt == 'q':
                self.enable = False
                return
            print(u'第%d页\t%s' % (page, story))

    def start(self):
        print(u'正在读取糗事百科，按回车查看新段子，输入q退出')
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # print(self.stories)
                # 从全局list中获取一页段子
                pageStroies = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStroy(pageStroies, nowPage)


spider = QSBK()
spider.start()
