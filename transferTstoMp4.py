# -*- coding: utf-8 -*-
import os
dirs = "/Users/renjm/Downloads/test/"
mp4 = "/Users/renjm/Downloads/mp4/"
# command1="ffmpeg -re -allowed_extensions ALL -protocol_whitelist 'file,http,crypto,tcp' -i '%sindex.m3u8' -c  copy out.ts" %dirs
# os.system(command1)
#ts文件绝对路径
 #读取ts文件夹下所有的ts文件
path_list = os.listdir(dirs)
 #对文件进行排序
path_list.sort()
 #将排序后的ts的绝对路径放入列表中
li = [os.path.join(dirs,filename) for filename in path_list]
cmd = ''
for file in li:
    if file != '/Users/renjm/Downloads/test/.DS_Store' and  file != '/Users/renjm/Downloads/test/vodkey.bin' and file!='/Users/renjm/Downloads/test/index.m3u8'and file!='/Users/renjm/Downloads/test/index.dl':
        file_path = os.path.join(dirs, file)
        cmd += file_path + '|'
            # print("文件：%s"%file_path)
cmd = cmd[:-1]
 #类似于[001.ts|00.2ts|003.ts]
input_file = cmd
 #指定输出文件名称
output_file = dirs+'1' + '.mp4'
 #使用ffmpeg将ts合并为mp4
command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s'%    (input_file,output_file)
 # 指行命令
os.system(command)
# filename = "d.mp4"
# a = 1
# content = ""
# lists = os.listdir(dirs)
# lists.sort()
# b = [lists[i:i + 250] for i in range(0, len(lists), 250)]
# for lis in b:
#     cmd = "cd %s && ffmpeg -i \"concat:" % mp4
#     for file in lis:
#         if file != '.DS_Store':
#             file_path = os.path.join(dirs, file)
#             cmd += file_path + '|'
#             # print("文件：%s"%file_path)
#     cmd = cmd[:-1]
#     cmd += '" -acodec copy -vcodec copy -absf aac_adtstoasc %s.mp4' % a
#     try:
#         os.system(cmd)
#         content += "file '%s.mp4'\n" % a
#         a = a + 1
#     except:
#         print("Unexpected error")

# fp = open("%smp4list.txt" % mp4, 'a+')
# fp.write(content)
# fp.close()
# mp4cmd = "cd %s && ffmpeg -i concat -i mp4list.txt -c copy %s" % (mp4,
#                                                                      filename)
# os.system(mp4cmd)