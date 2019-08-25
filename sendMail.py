'''
@Auther: renjm
@Date: 2019-08-13 13:13:59
@LastEditTime: 2019-08-25 20:49:36
@Description: 
'''
#coding:utf-8
#-*-coding:utf-8 -*-
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import yaml
import shutil
import requests


def sendEmail():
    config = {}
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(base_path + "/config.yaml") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    sender_email = config.get('sender')
    # receiver_email = config.get('receiver')
    m = MIMEMultipart()
    m['Subject'] = '风之动漫pdf版'
    password = config.get('password')
    comicPdfFolder = os.path.join(os.getcwd(), 'ComicPdf')
    comicFolder = os.path.join(os.getcwd(), 'Comic')
    if not os.listdir(comicPdfFolder):
        return
    for i in os.listdir(comicPdfFolder):
        if i == ".DS_Store":
            continue
        _comicPdfFolder = os.path.join(comicPdfFolder, i)
        _comicFolder = os.path.join(comicFolder, i)
        for file in os.listdir(_comicPdfFolder):

            pdfFile = os.path.join(_comicPdfFolder, file)
            fileName = file
            pdfApart = MIMEApplication(open(pdfFile, 'rb').read())
            pdfApart.add_header(
                'Content-Disposition', 'attachment', filename=fileName)
            m.attach(pdfApart)
            content = ' %s 第%s话' % (i, file.split('.')[0])
            textApart = MIMEText(content)
            requests.post(
                'http://127.0.0.1:3001/create/pdf',
                data={
                    'title': i,
                    'path': file
                })
            m.attach(textApart)
    server = smtplib.SMTP_SSL('smtp.qq.com')
    server.login(sender_email, password)
    server.sendmail(
        config.get('sender'), config.get('receiver'), m.as_string())
    server.quit()
    for _file in os.listdir(_comicPdfFolder):
        if _file == ".DS_Store":
            continue
        shutil.copyfile(
            os.path.join(_comicPdfFolder, _file),
            os.path.join('/Users/renjm/project/react/blogreact/', _file))
        os.remove(os.path.join(_comicPdfFolder, _file))
        path = _file.split('.')[0]
        comicPath = os.path.join(_comicFolder, path)
        for j in os.listdir(comicPath):
            if j == ".DS_Store":
                continue
            os.remove(os.path.join(comicPath, j))


sendEmail()
