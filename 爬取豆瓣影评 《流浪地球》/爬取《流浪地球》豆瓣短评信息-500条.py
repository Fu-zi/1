from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import re
import pandas as pd

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 QIHU 360EE'}

cookie_str = 'll="118281"; bid=uhPPtYyngE8; _vwo_uuid_v2=D0B7E524D0D23B241D34C50173330D210|4a16a20c19034064525f6c1356c6604b; __gads=ID=69808af367e4d943-228c1925a6c30009:T=1600828444:S=ALNI_MZ-4tSkVBTp7a8IT45rlnjSWo4M-g; __utmz=30149280.1600860455.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; __utma=30149280.1001933897.1600828432.1600828432.1600860455.2; ap_v=0,6.0; __utmt=1; dbcl2="216330669:uE6mTBf7x6E"; ck=NVQU; push_noty_num=0; push_doumail_num=0; douban-profile-remind=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1600860693%2C%22https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26266893%2F%22%5D; _pk_ses.100001.8cb4=*; __utmv=30149280.21633; __yadk_uid=wm7GowkbZKskQztGD6goP6skbEoBIBsj; _pk_id.100001.8cb4=3fd53cd655f15da0.1600829077.2.1600860815.1600829077.; __utmb=30149280.9.10.1600860455'
cookies = {}

for i in cookie_str.split(";"):
    key, values = i.split("=",1)
    cookies[key] = values

driver = webdriver.Chrome()

def get_info(url):
    # 1、获取网页源代码


    driver.get(url)
    wait = WebDriverWait(driver, 10)
    all_data = pd.DataFrame()
    page = 1                # 爬取的页数
    while True:
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,'#comments > div:nth-child(20) > div.comment > h3 >span.comment-info > a')))
        print('第'+str(page)+'页')
        # 开始循环爬数据
        dom = etree.HTML(driver.page_source,etree.HTMLParser(encoding='utf-8'))
        names = dom.xpath('//*[@class="comment-info"]/a/text()')  # 用户名
        user_pages = dom.xpath('//*[@class="comment-info"]/a/@href')   # 用户详细页

        citys = []
        user_infos = []
        for user_page in user_pages:    # 爬取详细页
            rq = requests.get(user_page, headers=headers)
            rq.content.decode(encoding='utf-8')
            link_dom = etree.HTML(rq.text, etree.HTMLParser(encoding='utf-8'))
            citys.append(link_dom.xpath('//*[@class="user-info"]/a/text()'))  # 居住城市
            user_infos.append(link_dom.xpath('//*[@class="user-info"]/div/text()'))  # 用户信息

        # 对详细页所爬取到的信息进行预处理
        citys = ['' if city == [] else city[0] for city in citys]
        join_times = ['' if user_infos==[] else user_infos[1] for user_info in user_infos]

        scores = dom.xpath('//*[@class="comment-info"]/span[2]/@class')             # 评分
        ['' if 'rating' not in scores else int(re.findall('[0-9]{2}', scores)[0]) for score in scores]
        comment_times = dom.xpath('//*[@class="comment-time "]/@title')      # 发表时间
        votes = dom.xpath('//*[@class="votes"]/text()')              # 赞同数量
        comments = dom.xpath('//*[@class="short"]/text()')           # 短评正文

        df = pd.DataFrame({
            '用户名：': names,
            '居住城市': citys,
            '入会时间': join_times,
            '用户评分': scores,
            '评论时间': comment_times,
            '赞同数量': votes,
            '短评正文': comments

        })

        print('所爬取到的第'+str(page)+'页数据\n', df)
        all_data = pd.concat([all_data, df], axis=0)               # 将每一页爬取到数据拼接到一块


        if(driver.find_elements_by_css_selector('#paginator>a.next')) ==[]:
            break
        # 定位后页
        confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#paginator > a.next')))
        confirm_btn.click()     # 单击后页进行翻页
        page = page + 1
    driver.close()
    all_data.to_csv('douban.csv')           #将数据进行存储




if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/26266893/comments?status=P'
    get_info(url)









