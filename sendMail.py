'''
@Auther: renjm
@Date: 2019-08-13 13:13:59
@LastEditTime: 2019-09-05 13:59:42
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
import oss2  # oss2包 连接阿里云OSS的工具


def sendEmail():
    config = {}
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(base_path + "/config.yaml") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    sender_email = config.get('sender')
    auth = oss2.Auth(config['oss']['accessKeyId'],
                     config['oss']['accessKeySecret'])  #详见文档
    endpoint = 'http://oss-cn-shanghai.aliyuncs.com'  #  地址
    bucket = oss2.Bucket(auth, endpoint, config['oss']['bucket'])  # 项目名称
    # receiver_email = config.get('receiver')
    m = MIMEMultipart()
    m['Subject'] = '风之动漫pdf版'
    m['To'] = config.get('receiver')
    m['From'] = sender_email
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
            bucket.put_object(
                os.path.join('comic', file),
                open(pdfFile, 'rb').read())
            # 这里发送请求去更新数据库中关于pdf的文件记录，后续继续调整
            requests.post(
                'http://127.0.0.1:3001/create/pdf',
                data={
                    'title': i,
                    'path': os.path.join('/comic', file)
                })
            m.attach(textApart)
        # 邮件内容整理好之后，清空pdf文件夹数据
        for _file in os.listdir(_comicPdfFolder):
            if _file == ".DS_Store":
                continue
            os.remove(os.path.join(_comicPdfFolder, _file))
            path = _file.split('.')[0]
            comicPath = os.path.join(_comicFolder, path)
            comicExists = os.path.exists(comicPath)
            if comicExists:
                for j in os.listdir(comicPath):
                    if j == ".DS_Store":
                        continue
                    os.remove(os.path.join(comicPath, j))
    # 发送邮件
    password = config.get('password')
    server = smtplib.SMTP_SSL('smtp.qq.com')
    server.login(sender_email, password)
    server.sendmail(
        config.get('sender'), config.get('receiver'), m.as_string())
    server.quit()


if __name__ == '__main__':
    sendEmail()
