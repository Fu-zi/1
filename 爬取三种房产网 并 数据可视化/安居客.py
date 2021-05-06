# -*- coding: utf-8 -*-

import pandas as pd
import requests
import time
import re
from selenium import webdriver
from multiprocessing import Process, Queue
import random
import csv

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
with open('anjuke_data.csv', 'a+', encoding='utf-8', newline='') as file:  # 创建文件对象
    writer = csv.writer(file)  # 为文件对象构建 csv写入对象
    writer.writerow(data_name)  # 写入csv文件内容

def anjuke_ygodwq_urls(page):
    # 安居客，粤港澳大湾区（广州、深圳、珠海、佛山、惠州、东莞、中山、江门）
    citys = ['guangzhou', 'foshan', 'shenzhen', 'zh', 'huizhou', 'dg', 'zs', 'jiangmen', 'zhaoqing']  # 各城市集合
    urls_anjuke = []
    for city in citys:
        url_anjuke = ['https://' + city + '.anjuke.com/sale/p{}/#'.format(str(i))
                      for i in range(1, page + 1)]  # 各城市的网页地址
        urls_anjuke.append(''.join(url_anjuke))  # 各城市的网页地址集合
    city_name = ['gz', 'fs', 'sz', 'zh', 'hui', 'dg', 'zs', 'jm', 'zq']
    return urls_anjuke, city_name

# 获取安居客子页面网站地址
def get_anjuke(url_anjuke, city, num):
    driver = webdriver.Chrome()  # 启动谷歌浏览器
    driver.get(url_anjuke)  # 发出请求
    html = driver.page_source  # 提取网页源码
    # 获得子页面链接
    links = re.findall('<a data-from="" data-company="" title=".*?href="(.*?)" target="_blank"', html)

    for link in links:
        time.sleep(4)
        get_info_anjuke(link, city, num)
        num += 1

# 获取安居客子页面信息
def get_info_anjuke(urls_anjuke, city, num):
    proxy_list = [
        'http://114.239.1.34:9999',
        'http://113.121.22.151:9999',
        'http://118.113.245.200:9999',
        'http://123.169.121.100:9999',
        'http://123.55.101.184:9999'
    ]
    proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    proxies = {'http': proxy_ip}
    response = requests.get(urls_anjuke, proxies=proxies, headers=headers, timeout=10).text
    # 房源名称
    name = re.findall('<h3 class="long-title">\s+(.*?)\s+</h3>', response)  # 正则表达式获取标题文本
    # 区域
    orientation = re.findall('<p class="loc-text"><a href=".*?" target="_blank" _soj=.*?>(.*?)</a>', response)
    # 房屋单价
    price = re.findall('房屋单价：</div>\s+<div class="houseInfo-content">(.*?) 元/m²</div>', response)
    # 建筑面积
    area = re.findall('建筑面积：</div>\s+<div class="houseInfo-content">(.*?)平方米</div>', response)
    # 房屋户型
    specifications = re.findall('<span class="info-tag"><em>(.*?)厅</span>', response)[0] + '厅'
    # 发布时间
    time = re.findall('发布时间：(.*?)</span>', response)
    # 配套资源
    resources = re.findall('配套电梯：</div>\s+<div class="houseInfo-content">(.*?)</div>', response)[0] + '配备电梯'

    datas = {
        'city': city,
        'name': name,
        'orientation': orientation,
        'price': price,
        'area': area,
        'specifications': format_data(specifications.split()),
        'time': time,
        'resources': resources.split(),
    }
    print(datas)
    # 字典中的key值即为csv中列名 ,行保存，默认为'columns',指定orient='columns'使用字典键
    dataframe = pd.DataFrame(datas, index=[num])
    # # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv(r"anjuke_data.csv", sep=',', header=False, mode='a', encoding='utf8')

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
        city = re.findall('https://(.*?).anjuke.com/sale/p.*?/#', str(url))[0]
        num_city = re.findall('https://.*?.anjuke.com/sale/p(.*?)/#', str(url))[0]
        # 爬取安居客各城市二手房信息数据
        get_anjuke(url, city, num) # 爬取链家各城市二手房信息数据
        time.sleep(2)
        print('爬取成功第' + num_city + '城市:'+ city)

    except Exception as e:
        print('Error: ', e)


if __name__ == '__main__':
    ProcessName = ["Process-1", "Process-2", "Process-3"]
    workQueue = Queue(1000)
    # 填充队列
    pages_anjuke= 23  # 爬取第一页
    i_anjuke = 0  # 爬取第一城市
    # 安居客楼盘名称、区域、单价、面积、户型、配套资源、发布时间
    for page_anjuke in range(1, pages_anjuke + 1):
        # 安居客，粤港澳大湾区各城市二手房网页地址集合及城市集合
        urls_anjukes, city_name = anjuke_ygodwq_urls(page_anjuke)
        for urls_anjuke in urls_anjukes:
            workQueue.put(urls_anjuke)
            for i in range(0, 3):
                    p = MyProcess(workQueue)
                    p.daemon = True
                    p.start()
                    p.join()

