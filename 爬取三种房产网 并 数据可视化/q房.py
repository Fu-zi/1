# -*- coding: utf-8 -*-

import pandas as pd
import requests
import time
import re
from selenium import webdriver
from multiprocessing import Process, Queue
import random
import csv
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36'}
data_name = ['city', 'name', 'orientation', 'price', 'area', 'specifications', 'time', 'resources']
num = 1  # 爬取楼盘序号

datas_name = {
    'city'
    'name'
    'orientation'
    'price'
    'area'
    'specifications'
    'time'
    'resources'}
with open('qfang_data.csv', 'a+', encoding='utf-8', newline='') as file:  # 创建文件对象
    writer = csv.writer(file)  # 为文件对象构建 csv写入对象
    writer.writerow(data_name)  # 写入csv文件内容


def qfang_ygodwq_urls(page):
    # Q房网，粤港澳大湾区（广州、深圳、珠海、佛山、惠州、东莞、中山、江门）
    citys = ['guangzhou', 'foshan', 'shenzhen', 'zh', 'huizhou', 'dg', 'zs', 'jiangmen', 'zhaoqing']  # 各城市集合
    urls_qfang = []
    for city in citys:
        url_qfang = ['https://' + city + '.qfang.com/rent/f{}'.format(str(i))
                      for i in range(1, page + 1)]  # 各城市的网页地址
        urls_qfang.append(''.join(url_qfang))  # 各城市的网页地址集合
    city_name = ['gz', 'fs', 'sz', 'zh', 'hui', 'dg', 'zs', 'jm', 'zq']
    return urls_qfang, city_name

# 获取Q房网子页面网站地址
def get_qfang(url_qfang, city, num):
    driver = webdriver.Chrome()  # 启动谷歌浏览器
    driver.get(url_qfang)  # 发出请求
    html = driver.page_source  # 提取网页源码

    soup = BeautifulSoup(html.text, 'lxml')
    links = soup.select('div > ul > li > div > div.list-main-header.clearfix > a').get('href')
    for link in links:
        time.sleep(2)
        get_info_qfang(link, city, num)
        num += 1

# 获取Q房网子页面信息
def get_info_qfang(urls_qfang, city, num):
    proxy_list = [
        'http://114.239.1.34:9999',
        'http://113.121.22.151:9999',
        'http://118.113.245.200:9999',
        'http://123.169.121.100:9999',
        'http://123.55.101.184:9999'
    ]
    proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    proxies = {'http': proxy_ip}
    response = requests.get(urls_qfang, proxies=proxies, headers=headers, timeout=10).text

    # 楼盘名称、区域、单价、面积、户型、配套资源、发布时间
    # 楼盘名称
    name = re.findall('insource=sale_detail_basic" target="_blank">(.*?)</a>', response)[0]
    # 区域
    orientation = re.findall('target="_blank" href="/sale.*?">(.*?)</a>', response)
    # 户型
    specifications = re.findall('\s<div class="text">(.*?)</div>', response)[0]

    # 租金
    price = re.findall('<span class="amount fl">(.*?)</span>', response)[0]
    # 面积
    area = re.findall('[\s\S]<p>(.*?)</p>', response)[1]
    # # 教育配套
    resources = re.findall('<a href="javascript:;" keyText="(.*?)" types=".*?>学校</a>', response)[0]

    datas = {
        'city': city,
        'name': name,
        'orientation': orientation[:1],
        'price': price,
        'area': area,
        'specifications': specifications,
        'time': time,
        'resources': resources.split(),
    }

    print(datas)
    # 字典中的key值即为csv中列名 ,行保存，默认为'columns',指定orient='columns'使用字典键
    dataframe = pd.DataFrame(datas, index=[num])
    # # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv(r"qfang_data.csv", sep=',', header=False, mode='a', encoding='utf8')


class MyProcess(Process):
    def __init__(self, q):
        Process.__init__(self)
        self.q = q

    def run(self):

        while not self.q.empty():
            crawler(self.q)


def crawler(q):
    try:
        url = q.get(timeout=2)
        city = re.findall('https://(.*?).qfang.com/sale/f.*?', str(url))[0]
        num_city = re.findall('https://.*?.qfang.com/sale/f(.*?)', str(url))[0]
        # 爬取Q房网各城市二手房信息数据
        get_qfang(url, city, num) # 爬取Q房网各城市二手房信息数据
        time.sleep(2)
        print('爬取成功第' + num_city + '城市:'+ city)

    except Exception as e:
        print('Error: ', e)


if __name__ == '__main__':
    ProcessName = ["Process-1", "Process-2", "Process-3"]
    workQueue = Queue(1000)
    # 填充队列
    pages_qfang= 23  # 爬取第一页
    num_city = 0  # 爬取第一城市
    # Q房网楼盘名称、区域、单价、面积、户型、配套资源、发布时间
    for page_qfang in range(pages_qfang):
        # Q房网，粤港澳大湾区各城市二手房网页地址集合及城市集合
        urls_qfangs, city_name = qfang_ygodwq_urls(page_qfang)
        for urls_qfang in urls_qfangs:
            workQueue.put(urls_qfang)
            for i in range(0, 3):
                    p = MyProcess(workQueue)
                    p.daemon = True
                    p.start()
                    p.join()

