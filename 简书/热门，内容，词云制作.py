# -*- coding: UTF-8 -*-
import requests
import time
import re
import csv
import pandas
import jieba
import jieba.analyse


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

#判断列表是否为空,(空格、制表符、换行符)，
def judge (list):
    if ''.join(list).isspace():
        list = '无'
    else:
        return list
    return list

#获取子页面网站地址
def get_info(url):

    response = requests.get(url, headers=headers).text
    titles = re.findall('<a class="title" target="_blank" href=".*?">(.*?)</a>', response)#标题
    contents = re.findall('class="abstract">.*?\n      (.*?)</p>', response, re.S)#文章内容

    with open('jianshu_hot.csv', 'a+', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['文章内容'])  #添加标题

    for title, contentt in zip(titles, contents):
        content = judge(contentt).replace(" ", "").split(" ")
        print("{} 爬取成功".format(title))
        with open('jianshu_hot.csv', 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow(content)  #添加数据

#Jieba分词并统计词频
def word_cloud():
            # 设置pd的显示列长度
            pandas.set_option('max_colwidth', 500)
            # 载入csv数据
            rows = pandas.read_csv('jianshu_hot.csv', encoding='utf-8', dtype=str)
            strs = []
            # 通过保存关键字的列表建立DataFrame
            dfstr = pandas.DataFrame(strs)
            # 词频统计，通过groupby函数从DataFrame中word的属性‘count’，求出总和
            dfword = dfstr.groupby('word')['count'].sum()
            #对Series的值进行前十降序排列
            print(dfword.sort_values(ascending=False)[0:10])
            # 保存为csv文件
            dfword.to_csv('jianshu_hot_词频.csv', encoding='utf-8')

if __name__ =='__main__':
    #爬取至第三页
    urls = ['https://www.jianshu.com/u/9104ebf5e177?order_by=top&page={}'.format(str(i))for i in range(1, 4)]# 爬取第一页25部电影
    for url in urls:
        get_info(url)
        time.sleep(2)

    word_cloud()