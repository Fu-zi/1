from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import time
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
cookies_str = 'bid=e6dANE-9UkU; ap_v=0,6.0; __utma=30149280.175772472.1599806312.1599806312.1599806312.1; __utmc=30149280; __utmz=30149280.1599806312.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __gads=ID=07bd73ab18bc57e7:T=1599806314:S=ALNI_MYdVnR0EkwVUz2Fp7ydgGAltDXeCw; ll="118281"; douban-fav-remind=1; _vwo_uuid_v2=DBDDE22B2C5DA3211B767F2E219AD46DA|e32433b2ad65b3a2ca4bc20efb969a13; __utmb=30149280.12.9.1599806366387'
cookes = {}
for i in cookies_str.split(';'):
    key, value = i.split('=', 1)
    cookes[key] = value


driver = webdriver.chrome()

def get_info(url):  #爬取特定一页豆瓣信息
    #获取网页源码
    driver.get(url)
    dom = etree.HTML(driver.page_source, etree.HTMLParser(encoding='utf-8'))
    wait = WebDriverWait(driver, 10)
    page = 1
    all_data = pd.DataFrame()
    while True:
        wait.until.EC.element_to_be_clickable(
            By.CSS_SELECTOR, '#comments > div:nth-child(20) > div.comment > h3 > span.comment-info >a'
        )
        print('第'+str(page)+'页')
    names = dom.xpath('//*[@class="comment-info"]/a/text()')  #用户名
    user_pages = dom.xpath('//*[@class="comment-info"]/a/@href')  #用户个人页面网址




if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/26266893/comments?status=P'
    get_info(url)