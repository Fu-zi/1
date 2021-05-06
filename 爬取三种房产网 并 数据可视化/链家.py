# -*- coding: utf-8 -*-

import pandas as pd
import requests
import time
import re
from selenium import webdriver
from multiprocessing import Process, Queue
import random
import csv
print('201806140055钱鹏')
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
with open('lianjia_data.csv', 'a+', encoding='utf-8', newline='') as file:  # 创建文件对象
    writer = csv.writer(file)  # 为文件对象构建 csv写入对象
    writer.writerow(data_name)  # 写入csv文件内容


def lianjie_ygodwq_urls(page):
    # 链家，粤港澳大湾区城市（广州、深圳、珠海、佛山、惠州、东莞、中山、江门）
    citys = ['gz', 'fs', 'sz', 'zh', 'hui', 'dg', 'zs', 'jiangmen']  # 各城市集合
    urls_lianjias = []
    for city in citys:
        urls_lianjia = ['https://' + city + '.lianjia.com/ershoufang/pg{}/'.format(str(page + 1))
                        ]  # 各城市的网页地址
        urls_lianjias.append(''.join(urls_lianjia))  # 各城市的网页地址集合
    city_name = ['gz', 'fs', 'sz', 'zh', 'hui', 'dg', 'zs', 'jm']

    return urls_lianjias, city_name

# 获取链家子页面网站地址
def get_lianjia(url_lianjia, city, num):
    driver = webdriver.Chrome()  # 启动谷歌浏览器
    driver.get(url_lianjia)  # 发出请求
    html = driver.page_source  # 提取网页源码

    # 获得子页面链接
    links = re.findall('<a class="" href="(.*?)" target="_blank" data-log_index=".*?" data-el="ershoufang" ',
                       html)  # 获得子页面链接
    for link in links:
        time.sleep(4)
        get_info_lianjia(link, city, num)
        num += 1

# 获取链家子页面信息
def get_info_lianjia(urls_lianjia, city, num):
    proxy_list = [
        'http://114.239.1.34:9999',
        'http://113.121.22.151:9999',
        'http://118.113.245.200:9999',
        'http://123.169.121.100:9999',
        'http://123.55.101.184:9999'
    ]
    proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    proxies = {'http': proxy_ip}
    response = requests.get(urls_lianjia, proxies=proxies, headers=headers, timeout=10).text

    # 楼盘名称、区域、单价、面积、户型、配套资源、发布时间
    # 房源名称
    name = re.findall('<h1 class="main" title="(.*?)">.*?</h1>', response)
    #
    orientation = re.findall('<a href="/ershoufang.*?/" target="_blank">(.*?)</a>&nbsp;', response)
    # 单价
    price = re.findall('<span class="unitPriceValue">(.*?)<i>', response)
    # 面积
    area = re.findall('<div class="area"><div class="mainInfo">(.*?)平米</div>', response)
    # 户型
    specifications = re.findall('<div class="room"><div class="mainInfo">(.*?)</div>', response)
    # 发布时间
    time = re.findall('<li>\s+<span class="label">挂牌时间</span>\s+<span>(.*?)</span>\s+</li>', response)
    # 配套资源
    resources = re.findall('<li><span class="label">配备电梯</span>(.*?)</li>', response)[0] + '配备电梯'

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
    dataframe.to_csv(r"lianjia_data.csv", sep=',', header=False, mode='a', encoding='utf8')

def format_data(s):
    return str(s).replace(" ", "").replace("\n", "").replace("\t", "").replace("/n", "").replace("<em>", "").replace(
        "</em>", "").replace("", "").strip()

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
        city = re.findall('https://(.*?).lianjia.com/ershoufang/', str(url))[0]
        num_city = re.findall('https://.*?.lianjia.com/ershoufang/pg(.*?)/', str(url))[0]
        # 爬取链家各城市二手房信息数据
        get_lianjia(url, city, num) # 爬取链家各城市二手房信息数据
        time.sleep(2)
        print('爬取成功第' + num_city + '城市:'+ city)

    except Exception as e:
        print('Error: ', e)


if __name__ == '__main__':
    ProcessName = ["Process-1", "Process-2", "Process-3"]
    workQueue = Queue(1000)
    # 填充队列
    pages_lianjia= 23  # 爬取第一页
    num_city = 0  # 爬取第一城市
    # 链家楼盘名称、区域、单价、面积、户型、配套资源、发布时间
    for page_lianjia in range(pages_lianjia):
        # 链家，粤港澳大湾区各城市二手房网页地址集合及城市集合
        urls_lianjias, city_name = lianjie_ygodwq_urls(page_lianjia)
        for urls_lianjia in urls_lianjias:
            workQueue.put(urls_lianjia)
            for i in range(0, 3):
                    p = MyProcess(workQueue)
                    p.daemon = True
                    p.start()
                    p.join()

