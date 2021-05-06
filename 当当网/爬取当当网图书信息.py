# -- coding: utf-8 --
print(201806140055,'钱鹏  大数据1802')

import requests
from lxml import etree
import csv
import sys
import io

#获取html对象并解析
def get_html(keywork):
    with open('当当网图书信息.csv', 'a+', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['书名', '折扣价', '定价', '作者', '出版时间', '出版社', '评论数', '简介'])
    url = 'http://search.dangdang.com/?'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    keywork = {'key': str(keywork)}
    response = requests.get(url, headers=header, params=keywork)    #获取网页源码
    response.content.decode(encoding='gbk')

    html = etree.HTML(response.text)  # 创建html对象
    li_list = html.xpath('//*[@id="component_59"]/li')  # xpath解析获取id为"component_59"下所有的li标签的内容
    specific_data(li_list)

#调整输出格式
def textStrip(s):
    return str(s).replace('¥', '').replace(" ", "").replace("\n", "").replace("\t", "").replace("", "").strip()

#获取指定信息
def specific_data(li_list):       #爬取特定信息
    for li in li_list:
        name = li.xpath('a[@class="pic"]/@title')[0]       #书名
        now_price = li.xpath('p[@class="price"]/span[@class="search_now_price"]/text()')[0]   #折扣价
        pre_price = li.xpath('p[@class="price"]/span[@class="search_pre_price"]/text()')[0]  #定价
        author = li.xpath('p[@class="search_book_author"]/span/a/text()')[0] #作者
        time = li.xpath('p[5]/span[2]/text()')[0].replace("/", "") #出版时间
        press = li.xpath('p[@class="search_book_author"]/span[3]/a/text()')[0]#出版社
        num = li.xpath('p[4]/a/text()')[0]#评论数

        introductions = li.xpath('p[2]/text()')
        if introductions:
            introduction = introductions[0]
        else:
            introduction = "无简介"#简介

        with open('当当网图书信息.csv', 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow((textStrip(name), textStrip(now_price), textStrip(pre_price),
                        textStrip(author), textStrip(time), textStrip(press), textStrip(num),
                        textStrip(introduction)))
            print(textStrip(name), textStrip(now_price), textStrip(pre_price),
                        textStrip(author), textStrip(time), textStrip(press), textStrip(num),
                        textStrip(introduction))

if __name__ == '__main__':

    get_html('机器学习' )