# -*- coding: utf-8 -*-

import scrapy
import sys
import os
import requests
import importlib
importlib.reload(sys)
import img2pdf
## 下载一拳超人漫画
from lxml import html
from renjm.items import RenjmItem
import re
##图片爬虫，使用到了 PhantomJS，因为 爬取的网站 是动态加载的，直接爬取会出现加载没完全的情况。现在使用phantomjs来等待加载完成
class ImageSpider(scrapy.Spider):
    name = "image"
    USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    # start_urls = ['https://manhua.fzdm.com/132/151']
    startUrl = 'https://manhua.fzdm.com/132/'
    headUrl = 'https://manhua.fzdm.com/132/151/'

    def start_requests(self):
        startUrls  =html.fromstring( requests.get(self.startUrl,headers=self.USER_AGENT).text)
        start = startUrls.xpath('//*[@id="content"]/li/a/@href')
        start_urls = []
        for url in start:
            exists = os.path.exists(os.path.join(os.getcwd(), 'Comic/%s'%url))
            if not exists:
                start_urls.append(self.startUrl+url)
               # os.makedirs(os.path.join(os.getcwd(), 'Comic/%s'%url))
        for i in start_urls:
            self.headUrl = i
            yield scrapy.Request(i, callback=self.parse)


    def parse(self, response):
        headUrl = self.headUrl
        comics_url_list = []
        com_count = response.xpath("//*[@id='pjax-container']/div[@class='navigation']")
        for i in com_count:
            com_url = i.xpath("./a/@href").extract()
            if (len(com_url)>3):
                for index in range(len(com_url)):
                    p = './a[%s]/text()' % index
                    comText = i.xpath(p).extract()
                    if(len(comText)!=0 and re.match('第', comText[0])):
                        url = headUrl + com_url[index-1]
                        comics_url_list.append(url)
            else:
                p = './a[%s]/text()' % (len(com_url) - 2)
                l = len(com_url) - 2
                comText = i.xpath(p).extract()
                if len(comText) is 0:
                    p = './a[%s]/text()' % (len(com_url) - 1)
                    l = len(com_url) - 1
                    comText = i.xpath(p).extract()
                if comText[0] != '下一页' and comText[0] != '上一页':
                    url = headUrl + com_url[l-1]
                    comics_url_list.append(url)
        print('\n>>>>>>>>>>>>>>>>>>> current page  list <<<<<<<<<<<<<<<<<<<<')
        print(comics_url_list)
        for url in comics_url_list:
            print('>>>>>>>> 动漫解析:' + url)
            _requests = scrapy.Request(url, callback=self.comics_parse)
            _requests.meta['PhantomJS'] = True
            yield _requests

    def comics_parse(self, response):
        comicImageUrl = response.xpath('//*[@id="mhpic"]/@src').extract()
        next_com_urls = response.xpath("//*[@id='pjax-container']/div[@class='navigation']")
        headUrl =  self.headUrl
        next_comics_url_list = []
        for i in next_com_urls:
            com_url = i.xpath("./a/@href").extract()
            p = './a[%s]/text()' % (len(com_url)-1)
            comText = i.xpath(p).extract()
            l = (len(com_url)-1)
            if comText[0] !='下一页':
                p = './a[%s]/text()' % (len(com_url))
                l = len(com_url)
                comText = i.xpath(p).extract()
            if comText[0] == '下一页':
                url = headUrl +com_url[l-1]
                next_comics_url_list.append(url)
        print(comicImageUrl)
        self.comicTitle = comicImageUrl[0]
        _requests =scrapy.Request(comicImageUrl[0], callback=self.content_parse)
        _requests.meta['notHtml'] = True
        _requests.meta['comicTitle'] = []
        if len(next_comics_url_list) != 0:
            _requests.meta['comicTitle'] = next_comics_url_list[0]
        if len(next_comics_url_list) == 0 and len(comicImageUrl) != 0:
            _requests.meta['comicTitle'] ='index_%s.html'% str(int(response.url.split('_')[1].split('.')[0])+1)
        yield _requests
        if len(next_comics_url_list) !=0:
            self.comicTitle = next_comics_url_list[0]
            _requests = scrapy.Request(next_comics_url_list[0], callback=self.comics_parse)
            _requests.meta['PhantomJS'] = True
            _requests.meta['comicTitle'] = next_comics_url_list[0]
            yield _requests


    def content_parse(self, response):
        folderName = self.headUrl.split('/')[-2]
        if len(response.meta['comicTitle']) == 0:
            return
        title = response.meta['comicTitle']
        document = os.path.join(os.getcwd(), 'Comic')
        folder_path = os.path.join(document, folderName)
        print('\n>>>>>>>>>>>>>>>>>>> folder_path  <<<<<<<<<<<<<<<<<<<<' +
              folder_path)
        exists = os.path.exists(folder_path)
        if not exists:
            print('create document: ' + folderName)
            os.makedirs(folder_path)
        fileName = folder_path + '/' + title.split('/')[-1] + '.jpg'
        url = response.url
        res = requests.get(url)
        item = RenjmItem()
        item['Name'] = fileName
        item['Content'] =res.content
        item['Status'] = res.status_code
        yield item


    # def save(self, title, content, folderName):
        # document = os.path.join(os.getcwd(), 'Comic')
        # folder_path = os.path.join(document, folderName)
        # print('\n>>>>>>>>>>>>>>>>>>> folder_path  <<<<<<<<<<<<<<<<<<<<' +
        #       folder_path)
        # exists = os.path.exists(folder_path)
        # if not exists:
        #     print('create document: ' + folderName)
        #     os.makedirs(folder_path)
        # fileName = folder_path + '/' + title.split('/')[-1] + '.jpg'
        # url = content.url
        # response = requests.get(url)
        # item = RenjmItem()
        # item['name'] = fileName
        # item['content'] =response.content
        # item['status'] = response.status_code
        # yield item
