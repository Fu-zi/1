from selenium import webdriver

url = 'https://movie.douban.com/subject/26266893/comments?status=P'
driver = webdriver.Firefox()
driver.get(url)
print(driver.page_source)


from lxml import etree
dom =  etree.HTML(driver.page_source,etree.HTMLParser(encoding='utf-8'))
names = dom.xpath('//*[@class="comment-info"]/a/text()')  # 用户名
user_pages = dom.xpath('//*[@class="comment-info"]/a/@href')   # 用户详细页

user_page = user_pages[0]


# 爬取详细信息
import requests
import re

citys = []
user_infos = []
for user_page in user_pages:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 QIHU 360EE'}
    rq = requests.get(user_page, headers=headers)
    rq.content.decode(encoding='utf-8')
    link_dom = etree.HTML(rq.text, etree.HTMLParser(encoding='utf-8'))
    citys.append(link_dom.xpath('//*[@class="user-info"]/a/text()'))  # 居住城市
    user_infos.append(link_dom.xpath('//*[@class="user-info"]/div/text()'))  # 用户信息

# 对详细页所爬取到的信息进行预处理
citys = ['' if city == [] else city[0] for city in citys]
join_times = ['' if user_infos==[] else user_infos[1] for user_info in user_infos]

scores = dom.xpath('//*[@class="comment-info"]/span[2]/@class') # 评分
['' if 'rating' not in scores else int(re.findall('[0-9]{2}',scores)[0]) for score in scores]
comment_times = dom.xpath('//*[@class="comment-info"]/span[3]/@title')  # 发表时间
votes = dom.xpath('//*[@class="votes"]/text()') # 赞同数量
comments = dom.xpath('//*[@class="short"]/text()')  # 短评正文



import pandas as pd
pd.DataFrame({
    '用户名：':names,
    '居住城市':citys,
    '入会时间':join_times,
    '用户评分':scores,
    '评论时间':comment_times,
    '赞同数量':votes,
    '短评正文':comments

})
















