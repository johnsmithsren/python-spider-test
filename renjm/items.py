# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy




class RenjmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field()
    Href = scrapy.Field()
    Content = scrapy.Field()
    Title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
