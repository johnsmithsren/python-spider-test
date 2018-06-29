# -*- coding: utf-8 -*-

import scrapy

from renjm.items import RenjmItem
import sys
from scrapy.selector import Selector
import json
import codecs
import requests
import os
reload(sys)

sys.setdefaultencoding('utf-8')


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # allowed_domains = ['www.biqukan.com/']
    start_urls = ['http://www.biqukan.com']

    def parse(self, response):
        # 获取单页中所有漫画的url
        comics_url_list = []
        com_count = response.xpath("//li/span[@class='s2']")
        for i in com_count:
            com_url = i.xpath("./a/@href").extract()
            url = 'http://www.biqukan.com' + com_url[0]
            comics_url_list.append(url)
        print('\n>>>>>>>>>>>>>>>>>>> current page  list <<<<<<<<<<<<<<<<<<<<')
        print(comics_url_list)
        for url in comics_url_list:
            print('>>>>>>>>  parse biqu:' + url)
            yield scrapy.Request(url=url, callback=self.comics_parse)

    def comics_parse(self, response):

        subSelector = response.xpath('//div[@class="listmain"]/dl/dd')
        for sub in subSelector:
            href = sub.xpath('./a/@href').extract_first()
            next_page = response.urljoin('http://www.biqukan.com' + href)
            print(
                '\n>>>>>>>>>>>>>>>>>>> current next page   <<<<<<<<<<<<<<<<<<<<'
                + next_page)

            yield scrapy.Request(next_page, callback=self.content_parse)

    def save(self, title, content, folderName):
        document = os.path.join(os.getcwd(), 'cartoon')
        folder_path = os.path.join(document, folderName)
        print('\n>>>>>>>>>>>>>>>>>>> folder_path  <<<<<<<<<<<<<<<<<<<<' +
              folder_path)
        exists = os.path.exists(folder_path)
        if not exists:
            print('create document: ' + folderName)
            os.makedirs(folder_path)
        fileName = folder_path + '/' + title + '.txt'
        with codecs.open(fileName, 'a', encoding='utf-8') as fp:
            c = json.dumps(content, ensure_ascii=False) + "\n"
            c = unicode.encode(c, 'utf-8')
            fp.write(json.loads(c))

    def content_parse(self, response):
        subSelector = response.xpath('//div[@class="content"]')
        folderName = response.xpath(
            '//div[@class="p"]/a[2]/text()').extract_first()
        for sub in subSelector:
            t = sub.xpath('./h1/text()').extract_first()
            print('\n>>>>>>>>>>>>>>>>>>> Ttile <<<<<<<<<<<<<<<<<<<<' + t)
            content = sub.xpath('./div[@class="showtxt"]').xpath(
                'string(.)').extract()[0].replace('\r', '').strip()
            self.save(t, content, folderName)
