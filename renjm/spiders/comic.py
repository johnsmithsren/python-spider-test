# -*- coding: utf-8 -*-

import scrapy

# from renjm.items import RenjmItem
import sys
# from scrapy.selector import Selector
import json
import codecs
import os
import requests
import importlib
importlib.reload(sys)
import img2pdf
from PIL import Image
from fpdf import FPDF
# sys.setdefaultencoding('utf-8')
## 下载一拳超人漫画
import io
from io import BytesIO
from lxml import html
class ImageSpider(scrapy.Spider):
    name = "image"
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # start_urls = ['https://manhua.fzdm.com/132/151']
    startUrl = 'https://manhua.fzdm.com/132/'
    headUrl = 'https://manhua.fzdm.com/132/151/'

    def start_requests(self):
        startUrls  =html.fromstring( requests.get(self.startUrl).text)
        start = startUrls.xpath('//*[@id="content"]/li/a/@href')
        start_urls = []
        for url in start:
            exists = os.path.exists(os.path.join(os.getcwd(), 'Comic/%s'%url))
            if not exists:
                start_urls.append(self.startUrl+url)
        for i in start_urls:
            yield scrapy.Request(i, callback=self.parse)


    def parse(self, response):
        headUrl = self.headUrl
        comics_url_list = []
        com_count = response.xpath("//*[@id='pjax-container']/div[@class='navigation']")
        for i in com_count:
            com_url = i.xpath("./a/@href").extract()
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
        _requests.meta['comicTitle'] = next_comics_url_list[0]
        yield _requests
        if len(next_comics_url_list) !=0:
            self.comicTitle = next_comics_url_list[0]
            _requests = scrapy.Request(next_comics_url_list[0], callback=self.comics_parse)
            _requests.meta['PhantomJS'] = True
            _requests.meta['comicTitle'] = next_comics_url_list[0]
            yield _requests


    def content_parse(self, response):
        folderName = self.headUrl.split('/')[-2]
        title = response.meta['comicTitle']
        self.save(title, response, folderName)


    def save(self, title, content, folderName):
        document = os.path.join(os.getcwd(), 'Comic')
        folder_path = os.path.join(document, folderName)
        print('\n>>>>>>>>>>>>>>>>>>> folder_path  <<<<<<<<<<<<<<<<<<<<' +
              folder_path)
        exists = os.path.exists(folder_path)
        if not exists:
            print('create document: ' + folderName)
            os.makedirs(folder_path)
        fileName = folder_path + '/' + title.split('/')[-1] + '.jpg'
        url = content.url
        response = requests.get(url)
        if response.status_code == 200:
            with open(fileName, 'wb') as f:
                f.write(response.content)
        comicFolder = os.path.join(os.getcwd(), 'Comic')
        for i in os.listdir(comicFolder):
            if i == ".DS_Store":
                return
            imgArray = []
            for f in os.listdir(os.path.join(comicFolder, i)):
                if f.endswith(".jpg"):
                    imgArray.append(os.path.join(os.path.join(comicFolder, i), f))
            pdf_bytes = img2pdf.convert(imgArray)
            file = open(os.path.join(comicFolder, i) + ".pdf", 'wb')
            file.write(pdf_bytes)
            file.close()