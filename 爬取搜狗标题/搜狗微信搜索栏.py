# -*- coding: utf-8 -*-
print(201806140055,'钱鹏  大数据1802')
import requests
from lxml import etree
url = 'https://weixin.sogou.com'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

#获取响应内容网站html页面并修改编码
response = requests.get(url, headers=header)
content = response.content.decode('utf-8')

html = etree.HTML(content)    # 创建html对象

lis = html.xpath('//*[@id="topwords"]/li/a/text()')      #获取所有li标签的a内容
for li in lis:
    print(li)
