# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
import codecs
import sys
import importlib
importlib.reload(sys)
# sys.setdefaultencoding('utf-8')


class RenjmPipeline(object):
    def process_item(self, item, spider):
        # now = time.strftime('%Y-%m-%d', time.localtime())
        fileName = item['Title'][0] + '.txt'
        with codecs.open(fileName, 'a', encoding='utf-8') as fp:
            for i in item['Content'][0]:
                str = json.dumps(i, ensure_ascii=False) + '\n'
                str = unicode.encode(str, 'utf-8')
                fp.write(str)
        return item
