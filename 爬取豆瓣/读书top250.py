import requests
from lxml import etree
import csv

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
urls = ['https://book.douban.com/top250?start={}'.format(str(i)) for i in range(0,50,25)]
file = open('douban.csv', 'wt', newline='', encoding='utf-8')  #创建csv文件
writer = csv.writer(file)
writer.writerow(('书名', '书的连接', '作者', '出版社', '出版日期', '价钱', '评分', '评价'))#读入标题
print('书名', '书的连接', '作者', '出版社', '出版日期', '价钱', '评分', '评价')

for url in urls:
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//tr[@class="item"]')
    for info in infos:
        name = info.xpath('td/div/a/@title')[0]
        href = info.xpath('td/div/a/@href')[0]
        book_infos = info.xpath('td/p/text()')[0]
        author = book_infos.split('/')[0]
        publisher = book_infos.split('/')[-3]
        date = book_infos.split('/')[-2]
        price = book_infos.split('/')[-1]
        rate = info.xpath('td/div/span[2]/text()')[0]
        comments = info.xpath('td/p/span/text()')
        if len(comments) != 0:
            comment = comments[0]
        else:
            comment = '空'

        print(name, href, author,publisher, date, price, rate, comment)
        writer.writerow((name, href, author, publisher, date, price, rate, comment))

