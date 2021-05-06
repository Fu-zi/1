print(201806140055,'钱鹏  大数据1802')
import requests
import time
import re
import pymongo

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


#获取子页面网站地址
def get_url(url):
    html = requests.get(url, headers=headers)
    links = re.findall('<a href="(.*?)" class="a_mask post_ulog post_ulog_action', html.text)  #获得子页面链接
    for link in links:
        time.sleep(2)
        get_info(link)

#获取子页面信息
def get_info(link):

    #房源名称、户型 、面积、坐向、总价、单价
    response = requests.get(link, headers=headers).text
    name = re.findall('<h3 class="detail_title">(.*?)</h3>', response)[0]  # 房源名称
    # 户型
    specifications = re.findall('<p class="gray big">房型</p><p class="red big">(.*?)</p></div>', response)[0]
    # 面积
    area = re.findall('<p class="gray big">建筑面积</p><p class="red big">(.*?)</p></div>', response)[0]
    # 坐向
    orientation = re.findall('<li class="short"><span class="gray">朝向：</span>(.*?)</li>', response)
    # 总价
    total_price = re.findall('<p class="red big"><span data-mark="price">(.*?)</span>', response)[0]+'元'
    #单价
    unit_Price= re.findall('<span class="gray">单价：</span>(.*?)</li>', response)[0]

    data = {
        '房源名称': name,
        '户型': specifications,
        '面积':  area,
        '坐向': ' '.join(orientation),
        '总价': total_price,
        '单价': unit_Price,
    }
    print(data)

    # 存储到mongodb数据库
    client = pymongo.MongoClient('localhost', 27017) # 链接数据库
    db = client['qp'] #创建数据库qp
    work = db.lianjia  # 在数据库qp里面创建表lianjia
    work.insert_one(dict(data)) #字典格式的数据导入mongodb数据库的lianjia表中


if __name__ =='__main__':
    urls = ['https://m.lianjia.com/gz/ershoufang/index/pg{}/'.format(str(i))for i in range(1, 2)]# 爬取第一页
    for url in urls:
        get_url(url)
        time.sleep(2)

