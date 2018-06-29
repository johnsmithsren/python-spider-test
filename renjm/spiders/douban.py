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
            url = 'http://www.biqukan.com/' + com_url[0]
            comics_url_list.append(url)
        print(
            '\n>>>>>>>>>>>>>>>>>>> current page comics list <<<<<<<<<<<<<<<<<<<<'
        )
        print(comics_url_list)
        for url in comics_url_list:
            print('>>>>>>>>  parse comics:' + url)
            yield scrapy.Request(url=url, callback=self.comics_parse)

        # subSelector = response.xpath('//div[@class="content"]')
        # for sub in subSelector:
        #     item = RenjmItem()
        #     item['Title'] = []
        #     item['Content'] = []
        #     t = sub.xpath('./h1/text()').extract_first()
        #     content = sub.xpath('./div[@class="showtxt"]/text()').extract()
        #     item['Title'].append(t)
        #     item['Content'].append(content)
        #     yield item
        # next_href = response.xpath(
        #     '//div[@class="page_chapter"]/ul/li[3]/a/@href').extract()
        # if next_href is not None:
        #     next_page = response.urljoin(
        #         'http://www.biqukan.com/' + next_href[0])
        # yield scrapy.Request(next_page, callback=self.parse)

    def comics_parse(self, response):
        # 提取每部漫画数据
        content = Selector(response=response)
        if not content:
            print('parse comics body error.')
            return

        subSelector = response.xpath('//div[@class="listmain"]/dl/dd')
        for sub in subSelector:
            # item = RenjmItem()
            # item['Title'] = []
            # item['Content'] = []
            t = sub.xpath('./a/text()').extract_first()
            # content = sub.xpath('./div[@class="showtxt"]/text()').extract()
            self.save(t)
            # 将图片保存到本地
            # self.save(t, content)

        # 下一页图片的url，当下一页标签的href属性为‘#’时为漫画的最后一页

        # next_href = response.xpath(
        #     '//div[@class="page_chapter"]/ul/li[3]/a/@href').extract()
        # if next_href is not None:
        #     next_page = response.urljoin(
        #         'http://www.biqukan.com/' + next_href[0])
        # yield scrapy.Request(next_page, callback=self.comics_parse)

    def save(self, title):
        # 将图片保存到本地
        # self.log('saving pic: ' + img_url)

        # 保存漫画的文件夹
        document = os.path.join(os.getcwd(), 'cartoon')

        # 每部漫画的文件名以标题命名
        comics_path = os.path.join(document, title)
        exists = os.path.exists(comics_path)
        if not exists:
            print('create document: ' + title)
            os.makedirs(comics_path)

        # 每张图片以页数命名
        # pic_name = comics_path + '/' + img_mun + '.jpg'

        # # 检查图片是否已经下载到本地，若存在则不再重新下载
        # exists = os.path.exists(pic_name)
        # if exists:
        #     print('pic exists: ' + pic_name)
        #     return
        fileName = comics_path + '/' + title + '.txt'
        with codecs.open(fileName, 'a', encoding='utf-8') as fp:
            str = json.dumps(title, ensure_ascii=False) + '\n'
            str = unicode.encode(str, 'utf-8')
            fp.write(str)
        # try:
        #     response = requests.get(img_url, timeout=30)

        #     # 请求返回到的数据
        #     data = response

        #     with open(pic_name, 'wb') as f:
        #         for chunk in data.iter_content(chunk_size=1024):
        #             if chunk:
        #                 f.write(chunk)
        #                 f.flush()

        #                 print('save image finished:' + pic_name)

        # except Exception as e:
        #     print('save image error.')
        #     print(e)