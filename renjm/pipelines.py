'''
@Auther: renjm
@Date: 2019-07-13 23:37:58
@LastEditTime: 2019-08-25 17:11:19
@Description: 
'''
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
import os
import img2pdf


class RenjmPipeline(object):
    def process_item(self, item, spider):
        # now = time.strftime('%Y-%m-%d', time.localtime())
        if item['Status'] == 200:
            with open(item['Name'], 'wb') as f:
                f.write(item['Content'])
                f.close()
        return item

    def close_spider(self, spider):
        comicFolder = os.path.join(os.getcwd(), 'Comic')
        comicPdfFolder = os.path.join(os.getcwd(), 'ComicPdf')
        for j in os.listdir(comicFolder):
            _comicFolder = os.path.join(comicFolder, j)
            _comicPdfFolder = os.path.join(comicPdfFolder, j)
            _comicPdfExists = os.path.exists(_comicPdfFolder)
            if not _comicPdfExists:
                print('create document: ' + j)
                os.makedirs(_comicPdfFolder)
            for i in os.listdir(_comicFolder):
                if i == ".DS_Store":
                    continue
                imgArray = []
                for f in os.listdir(os.path.join(_comicFolder, i)):
                    if f.endswith(".jpg"):
                        imgArray.append(
                            os.path.join(os.path.join(_comicFolder, i), f))
                if len(imgArray) == 0:
                    continue
                imgArray = sorted(
                    imgArray,
                    key=lambda x: int((x.split('_')[1]).split('.')[0]))
                pdf_bytes = img2pdf.convert(imgArray)
                file = open(os.path.join(_comicPdfFolder, i) + ".pdf", 'wb')
                file.write(pdf_bytes)
                file.close()
        return
