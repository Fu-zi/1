print("201806140055,钱鹏，大数据1802")
from bs4 import BeautifulSoup
import requests
import time
import re
import os
from lxml import etree

#包括出租房源的小区名称、特点、户型、
# 面积、租金、登记经纪人及房源图片。
#调整输出格式
def textStrip(s):
    return str(s).replace('[', '').replace("]", "").replace("\n", "").replace("\r", "").replace(" ", "").strip()


def get_url(url):        #获取子页面网站地址
        response = requests.get(url, headers=header,proxies=proxy, timeout=3)
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.select('div > ul > li > div > div.list-main-header.clearfix > a')

        return links

# def specific_data_bs4(url):         #爬取特定网页数据
#     links = get_url(url)    #获取子页面网站地址
#     for link in links:
#         href = link.get('href')
#         url_href = 'https://shenzhen.qfang.com/'+href #子页面网站
#         response = requests.get(url_href, headers = header)
#         soup = BeautifulSoup(response.text, 'lxml')
#
#         #楼盘名称
#         names = soup.select('#headInfo > div > div.head-side.fl > div.head-list > ul > li:nth-child(1) > div.text.fl > a')
#         #户型
#         house_types = soup.select('#scrollto-2 > div.house-info.clearfix > ul > li:nth-child(1) > div.text')
#         # 面积
#         areas = soup.select('#scrollto-2 > div.house-info.clearfix > ul > li:nth-child(3) > div.text')
#         #楼层
#         floors = soup.select('#scrollto-2 > div.house-info.clearfix > ul > li:nth-child(2) > div.text')
#         #租金
#         rents = soup.select(' #headInfo > div > div.head-side.fl > div.head-side-top.clearfix > div.head-side-price.fl > span')
#         #区域
#         regions = soup.select('#headInfo > div > div.head-side.fl > div.head-list > ul > li:nth-child(4) > div.crop-wrap.fl.clearfix > div')
#         #教育配套
#         matchings = soup.find_all('p',class_="map-layer-tabs clearfix")
#
#         for name,house_type,area,rent,floor,region,matching in zip(names,house_types,areas,rents,floors,regions,matchings):
#             data = {'出租房源的楼盘名称为：':name.get_text().strip(),
#                    '户型':house_type.get_text().strip(),
#                    '面积':area.get_text().strip(),
#                     '楼层': floor.get_text().strip(),
#                    '租金':rent.get_text().strip()+'元/月',
#                     '区域': textStrip(region.get_text()),
#                     '教育配套': textStrip(re.findall('.*keytext="(.*?)".*?>学校',str(matching)))
#                     }
#             print(data)


def specific_data_lxml(url):
    links = get_url(url)    #获取子页面网站地址
    for link in links:
        href = link.get('href')
        url_href = 'https://shenzhen.qfang.com/'+href #子页面网站
        response = requests.get(url_href, headers=header, proxies=proxy, timeout=3)
        html = etree.HTML(response.text)
        #楼盘名称
        names = html.xpath('//*[@id="headInfo"]/div/div[2]/div[3]/ul/li[1]/div[2]/a/text()')[0]
        #户型
        house_types =html.xpath('//*[@id="scrollto-2"]/div[2]/ul/li[1]/div[2]/text()')[0]
        #面积
        areas = html.xpath('//*[@id="scrollto-2"]/div[2]/ul/li[3]/div[2]/text()')[0]
        #楼层
        floors = html.xpath('//*[@id="scrollto-2"]/div[2]/ul/li[2]/div[2]/text()')[0]
        #租金
        rents = html.xpath('//*[@id="headInfo"]/div/div[2]/div[1]/div[1]/span/text()')[0]
        #区域
        regions1 = html.xpath('//*[@id="headInfo"]/div/div[2]/div[3]/ul/li[4]/div[2]/div/a[1]/text()')
        regions2 = html.xpath('//*[@id="headInfo"]/div/div[2]/div[3]/ul/li[4]/div[2]/div/a[2]/text()')
        # 教育配套
        matchings = html.xpath('//*[@id="mapFuncsTbs"]/a[2]/text()')[0]
        data = {'出租房源的楼盘名称为：':names,
                   '户型':house_types,
                   '面积':areas,
                    '楼层': textStrip(floors),
                   '租金':rents+'元/月',
                    '区域': textStrip(regions1)+textStrip(regions2),
                    '教育配套': textStrip(matchings)
                    }
        print(data)
def text(text):     #正则表达式筛选文本
    # name = re.findall('[\u4e00-\u9fa5]', str(text))
    pattern = re.compile(r'\s|\n|<.*?>', re.S)
    # 将匹配到的内容用空替换，即去除匹配的内容，只留下文本
    name = pattern.sub('', str(text))
    return "".join(name)

def specific_data_re(url):
    links = get_url(url)  # 获取子页面网站地址
    for link in links:
        href = link.get('href')
        url_href = 'https://shenzhen.qfang.com/' + href  # 子页面网站
        response = requests.get(url_href, headers=header, proxies=proxy, timeout=3).text
        # 楼盘名称
        names = re.findall('target="_blank">(.*?)</a>',response)[0]
        #户型
        house_types = re.findall('<li class ="items left">\t<p>(.*?)</p>',response)[0]
        # 面积
        areas = re.findall('<div class="text">(.*?)</div> ',response)[0]
        # 楼层
        floors = re.findall('<li class ="items left">\t<span>(.*?).*</span>')[0]
        # 租金
        rents = re.findall('<span class="amount fl">(\d*)</span> ',response)[0]
        # 区域
        regions = re.findall('target="_blank".*?">(.*?)</a> ',response)[0]
        # 教育配套
        matchings = re.findall('keytext="(.*?)".*?学校</a>',response)[0]
        data = {'出租房源的楼盘名称为：': names,
                '户型': house_types,
                '面积': areas,
                '楼层': textStrip(floors),
                '租金': rents + '元/月',
                '区域': textStrip(regions),
                '教育配套': textStrip(matchings)
                }

#楼盘名称，户型，面积，楼层，租金，区域，教育配套
if __name__ == '__main__':
    ip = '121.237.148.143:3000'
    proxy = {
        'http': 'http://' + ip,
        'https': 'https://' + ip
    }

    header = {'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
          'like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    urls = ["https://shenzhen.qfang.com/rent/f{}".format(num)
            for num in range(1, 2)] #所爬取网页
    for url in urls:
        time.sleep(1)
        # start_timeb = time.time()  # 记录程序开始运行时间
        # specific_data_bs4(url)
        # end_timeb = time.time()  # 记录程序结束运行时间
        # print('BeautifulSoup库的运行时间：',end_timeb - start_timeb)

        start_timeL = time.time()  # 记录程序开始运行时间
        specific_data_lxml(url)
        end_timeL = time.time()  # 记录程序结束运行时间
        # print('Lxml 库的 xpath的运行时间：',end_timeL - start_timeL)