'''
@Auther: renjm
@Date: 2019-08-13 13:13:59
@LastEditTime: 2019-08-13 13:31:03
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


def sendEmail():
    config = {}
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(base_path + "/config.yaml") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    sender_email = config.get('sender')
    receiver_email = config.get('receiver')
    password = config.get('password')
    content = '一拳超人'
    textApart = MIMEText(content)
    comicPdfFolder = os.path.join(os.getcwd(), 'ComicPdf')
    comicFolder = os.path.join(os.getcwd(), 'Comic')
    m = MIMEMultipart()
    m.attach(textApart)
    if not os.listdir(comicPdfFolder):
        return
    for i in os.listdir(comicPdfFolder):
        if i == ".DS_Store":
            continue
        pdfFile = os.path.join(comicPdfFolder, i)
        fileName = i
        pdfApart = MIMEApplication(open(pdfFile, 'rb').read())
        pdfApart.add_header(
            'Content-Disposition', 'attachment', filename=fileName)
        m.attach(pdfApart)
    m['Subject'] = 'comicPdf'
    # context = ssl.create_default_context()
    # server = smtplib.SMTP_SSL('smtp.qq.com')
    # server.login(sender_email, password)
    # server.sendmail(config.get('sender'), config.get('receiver'),
    #                 m.as_string())
    # server.quit()
    for i in os.listdir(comicPdfFolder):
        if i == ".DS_Store":
            continue
        shutil.copyfile(
            os.path.join(comicPdfFolder, i),
            os.path.join('/Users/renjm/project/react/blogreact/', i))
        os.remove(os.path.join(comicPdfFolder, i))
        path = i.split('.')[0]
        comicPath = os.path.join(comicFolder, path)
        for j in os.listdir(comicPath):
            if j == ".DS_Store":
                continue
            os.remove(os.path.join(comicPath, j))


sendEmail()
