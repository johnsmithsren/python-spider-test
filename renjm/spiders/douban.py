# -*- coding: utf-8 -*-

import scrapy

from renjm.items import RenjmItem
import sys
# import json
reload(sys)
sys.setdefaultencoding('utf-8')


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # allowed_domains = ['www.biqukan.com/']
    start_urls = ['http://www.biqukan.com/0_784/16308189.html']

    def parse(self, response):
        start = 
        subSelector = response.xpath('//div[@class="content"]')
        for sub in subSelector:
            item = RenjmItem()
            item['Title'] = []
            item['Content'] = []
            t = sub.xpath('./h1/text()').extract_first()
            content = sub.xpath('./div[@class="showtxt"]/text()').extract()
            item['Title'].append(t)
            item['Content'].append(content)
            yield item
        next_href = response.xpath(
            '//div[@class="page_chapter"]/ul/li[3]/a/@href').extract()
        if next_href is not None:
            next_page = response.urljoin(
                'http://www.biqukan.com/' + next_href[0])
        yield scrapy.Request(next_page, callback=self.parse)
