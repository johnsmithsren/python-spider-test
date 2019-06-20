# # -*- coding:utf-8 -*-
# import sys, click, re, base64, binascii, json, os
# import crypto
# import sys
# sys.modules['Crypto'] = crypto
# from Crypto.Cipher import AES
# from http import cookiejar
# import scrapy
# from scrapy import Spider
# from scrapy.selector import Selector
# # from urllib.parse import quote
# # from scrapysplashtest.items import ProductItem
# from scrapy_splash import SplashRequest
#
# # from renjm.items import RenjmItem
# # import sys
# # from scrapy.selector import Selector
# # import json
# # import codecs
# import requests
# # import os
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# script = """
#     function main(splash, args)
#     splash.images_enabled = false
#     assert(splash:go(args.url))
#     assert(splash:wait(args.wait))
#     js = string.format("document.querySelector('#mainsrp-pager div.form > input').value=%d;document.querySelector('#mainsrp-pager div.form > span.btn.J_Submit').click()", args.page)
#     splash:evaljs(js)
#     assert(splash:wait(args.wait))
#     return splash:html()
#     end
#     """
#
#
# class NetEaseMusicSpider(scrapy.Spider):
#     name = "music"
#     USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
#
#     allowed_domains = ['music.163.com']
#
#     # start_urls = ['https://music.163.com/#/discover/toplist']
#
#     def start_requests(self):
#         url = 'http://music.163.com/#/discover/toplist'
#         yield SplashRequest(
#             url, callback=self.parse, endpoint='render.html', args={
#                 'wait': 5
#             })
#
#     def parse(self, response):
#         res = response
#         print res.text
#         # com_count = res.xpath(
#         #     "//*[@id='5692002121530663575803']/td[2]/div/div").extract_first()
#         print(u'----------使用splash获取异步加载内容-----------')
#         guessyou = res.xpath('//tbody/tr').extract_first()
#         print(u"find：%s" % guessyou)
#         print(u'---------------success----------------')
#
#         # print('\n>>>>>>>>:' + com_count)
#         # for i in com_count:
#         #     musicId = i.xpath(
#         #         "./td[2]/div/div/span/@data-res-id").extract_first()
#
#         #     musicTitle = i.xpath(
#         #         "./td[2]/div/div/div/span/a/b/@title").extract_first()
#         #     print('\n>>>>>>>> music title:' + musicTitle)
#         #     print('\n>>>>>>>>  download music:')
#         #     self.loadMusic(musicId, musicTitle)
#         # yield scrapy.Request(url=url, callback=self.comics_parse)
#
#     def loadMusic(self, musicId, musicTitle):
#         music = Music('.')
#         music.download_song_by_id(musicId, musicTitle, 2)
#
#
# #下载网易云音乐需要进行加密验证，这里引入Jack-Cherish/python-spider中的加密解密，方便请求
# class Encrypyed():
#     def __init__(self):
#         self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
#         self.nonce = '0CoJUm6Qyw8W8jud'
#         self.pub_key = '010001'
#
#     # 加密算法可以通过观察网易云音乐的core.js文件，获取其中的加密算法得出，后续有了加密算法，就可以请求网易云音乐的一般接口获取音乐下载地址。
#     def encrypted_request(self, text):
#         text = json.dumps(text)
#         sec_key = self.create_secret_key(16)
#         enc_text = self.aes_encrypt(
#             self.aes_encrypt(text, self.nonce), sec_key.decode('utf-8'))
#         enc_sec_key = self.rsa_encrpt(sec_key, self.pub_key, self.modulus)
#         data = {'params': enc_text, 'encSecKey': enc_sec_key}
#         return data
#
#     def aes_encrypt(self, text, secKey):
#         pad = 16 - len(text) % 16
#         text = text + chr(pad) * pad
#         encryptor = AES.new(
#             secKey.encode('utf-8'), AES.MODE_CBC, b'0102030405060708')
#         ciphertext = encryptor.encrypt(text.encode('utf-8'))
#         ciphertext = base64.b64encode(ciphertext).decode('utf-8')
#         return ciphertext
#
#     def rsa_encrpt(self, text, pubKey, modulus):
#         text = text[::-1]
#         rs = pow(
#             int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
#         return format(rs, 'x').zfill(256)
#
#     def create_secret_key(self, size):
#         return binascii.hexlify(os.urandom(size))[:16]
#
#
# class Crawler():
#     def __init__(self):
#         self.headers = {
#             'Accept':
#             '*/*',
#             'Accept-Encoding':
#             'gzip,deflate,sdch',
#             'Accept-Language':
#             'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
#             'Connection':
#             'keep-alive',
#             'Content-Type':
#             'application/x-www-form-urlencoded',
#             'Host':
#             'music.163.com',
#             'Referer':
#             'http://music.163.com/search/',
#             'User-Agent':
#             'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
#         }
#
#         self.session = requests.Session()
#         self.session.headers.update(self.headers)
#         self.download_session = requests.Session()
#         self.ep = Encrypyed()
#
#     def get_song_by_url(self, song_url, song_name, folder):
#         """
#             :params song_url: 歌曲下载地址
#             :params song_name: 歌曲名字
#             :params song_num: 下载的歌曲数
#             """
#         document = os.path.join(os.getcwd(), 'Music')
#         folder_path = os.path.join(document, song_name)
#         resp = self.download_session.get(song_url, stream=True)
#         exists = os.path.exists(folder_path)
#         if not exists:
#             os.makedirs(folder_path)
#         fpath = os.path.join(folder_path, song_name + '.mp3')
#         with open(fpath, 'a') as song_file:
#             for chunk in resp.iter_content(chunk_size=1024):
#                 if chunk:
#                     song_file.write(chunk)
#
#     def post_request(self, url, params):
#         data = self.ep.encrypted_request(params)
#         resp = self.session.post(url, data=data)
#         result = resp.json()
#         return result
#
#     def get_song_url(self, song_id, bit_rate=320000):
#         url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
#         csrf = ''
#         params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
#         result = self.post_request(url, params)
#         # 歌曲下载地址
#         song_url = result['data'][0]['url']
#         return song_url
#
#
# class Music():
#     def __init__(self, folder):
#         self.crawler = Crawler()
#         self.folder = '.' if folder is None else folder
#
#     def download_song_by_id(self, song_id, song_name, folder='.'):
#
#         url = self.crawler.get_song_url(song_id)
#         # 去掉非法字符
#         song_name = song_name.replace('/', '')
#         song_name = song_name.replace('.', '')
#         self.crawler.get_song_by_url(url, song_name, folder)
