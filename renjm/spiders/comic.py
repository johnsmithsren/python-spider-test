'''
@Auther: renjm
@Date: 2019-07-18 11:51:47
@LastEditTime: 2019-09-21 13:13:46
@Description: 
'''
# -*- coding: utf-8 -*-
# import img2pdf
from lxml import html
from renjm.items import RenjmItem
import scrapy
import sys
import os
import requests
import importlib
importlib.reload(sys)
from selenium import webdriver
requests.packages.urllib3.disable_warnings()


##图片爬虫，使用到了 PhantomJS，因为 爬取的网站 是动态加载的，直接爬取会出现加载没完全的情况。现在使用phantomjs来等待加载完成
class ImageSpider(scrapy.Spider):
    name = "image"
    USER_AGENT = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    startUrls = [
        'https://www.manhuadui.com/manhua/haizeiwang/',
        'https://www.manhuadui.com/manhua/yiquanchaoren/'
    ]

    def start_requests(self):
        headUrl = 'https://www.manhuadui.com'
        # 起始的链接列表
        for startUrl in self.startUrls:
            # 接下来需要请求的漫画的列表页请求集合
            startUrlList = []
            # 创建chrome启动选项
            chrome_options = webdriver.ChromeOptions()
            # 指定chrome启动类型为headless 并且禁用gpu
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            # 调用环境变量指定的chrome浏览器创建浏览器对象
            driver = webdriver.Chrome(
                '/Users/renjm/project/scrapy/chromedriver',
                chrome_options=chrome_options)
            driver.implicitly_wait(30)
            driver.get(startUrl)
            # 请求页面的元素集合
            pageElementList = html.fromstring(driver.page_source)
            # 请求页面的列表页面元素集合
            aTagList = pageElementList.xpath('//*[@id="chapter-list-1"]/li/a')
            # 漫画页面列表的标题集合，用户创建文件夹
            comicTitle = pageElementList.xpath(
                "/html/body/div[3]/div[1]/div[1]/div[2]/h1/text()")[0]
            for element in aTagList:
                title = element.xpath('./@title')[0]
                href = element.xpath('./@href')[0]
                exists = os.path.exists(
                    os.path.join(os.getcwd(),
                                 'Comic/%s/%s' % (comicTitle, title)))
                if not exists:
                    # os.makedirs(
                    #     os.path.join(os.getcwd(),
                    #                  'Comic/%s/%s' % (comicTitle, title)))
                    startUrlList.append(headUrl + href)
            for comicListUrl in startUrlList:
                self.headUrl = comicListUrl
                self.folderTitle = comicTitle
                comicFirstPageResponse = scrapy.Request(
                    comicListUrl, callback=self.parse)
                comicFirstPageResponse.meta['folderTitle'] = comicTitle
                yield comicFirstPageResponse

    def parse(self, comicFirstPageResponse):
        headUrl = comicFirstPageResponse.url
        subComicPageUrlList = []
        pageCount = comicFirstPageResponse.xpath(
            "//*[@id='images']/p/text()")[0].root
        totalPage = pageCount.split('/')[1].split(')')[0]
        print('\n>>>>>>>>>>>>>>>>>>> Total Page <<<<<<<<<<<<<<<<<<<<')
        print(totalPage)
        subComicPageUrlList.append(headUrl)
        for i in range(int(totalPage)):
            subComicPageUrlList.append(headUrl + '?p=%s' % i)
        print(subComicPageUrlList)
        for subComicPageUrl in subComicPageUrlList:
            print('>>>>>>>> 开始漫画页面请求:' + subComicPageUrl)
            imageRequests = scrapy.Request(
                subComicPageUrl, callback=self.comics_parse)
            imageRequests.meta['PhantomJS'] = True
            imageRequests.meta['responseUrl'] = comicFirstPageResponse.url
            yield imageRequests

    def comics_parse(self, response):
        # 漫画的名称
        comicFolderName = response.xpath(
            "/html/body/div[2]/div[1]/div/h1/a/text()").extract_first()
        # 当前话数的标题
        title = response.xpath(
            "/html/body/div[2]/div[1]/div/h2/text()").extract_first()
        # 漫画文件夹名称
        document = os.path.join(os.getcwd(), 'Comic/%s' % comicFolderName)
        # 漫画具体话数图片存放路径
        folder_path = os.path.join(document, title)
        exists = os.path.exists(folder_path)
        if not exists:
            print('create document: ' + folder_path)
            os.makedirs(folder_path)
        page = response.xpath("//*[@id='images']/p/text()").extract_first()
        fileName = folder_path + '/' + page.split('/')[0].split(
            '(')[1] + '.png'
        url = response.xpath('//*[@id="images"]/img/@src').extract_first()
        res = requests.get(url)
        item = RenjmItem()
        item['Name'] = fileName
        item['Content'] = res.content
        item['Status'] = res.status_code
        yield item
