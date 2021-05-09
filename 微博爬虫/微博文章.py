#-*- coding:utf-8 -*-
from selenium import webdriver
import time
import re
import csv
import jieba
import pandas
import jieba.analyse
from wordcloud import WordCloud     #导入子包，节约资源
import matplotlib.pyplot as plt     #下载matplotlib包

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
driver = webdriver.Chrome()  # 启动谷歌浏览器
# driver.maximize_window()#将浏览器最大化

def get_selenium(url,page,word):

    #打开搜索页面窗口
    driver.get(url)  # 发出请求
    driver.implicitly_wait(20)   # 隐式等待,显示等待搜索页面全部渲染完成
    time.sleep(2)
    # 点击登录框,弹出登录框
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div[2]/ul/li[3]/a').click()
     # 定位账号输入文本框并输入账号信息至文本框

    # 定位账号输入文本框并输入账号信息至文本框
    time.sleep(2)
    driver.find_element_by_name("username").send_keys('18579218484')

    # 定位密码输入文本框并输入密码信息至文本框
    driver.find_element_by_name("password").send_keys('a123456')

    # 定位登录按钮并进行点击
    time.sleep(2)
    driver.find_element_by_class_name('item_btn').click()


    #因微博网页有特殊设置原因，在登录账号后，登录信息框未消失，需点击取消或者直接输入关键词搜索，才能进行随后操作
    # 定位搜索框并输入搜索关键词
    time.sleep(8)   #因微博的反爬虫机制，在频繁登录爬取时，将会提示报错“打开界面元素未加载完成，点击会报错”加长等待时间即可成果运行
    driver.find_element_by_xpath('//*[@id="weibo_top_public"]/div/div/div[2]/input').send_keys(word)
    driver.find_element_by_xpath('//*[@id="weibo_top_public"]/div/div/div[2]/a').click() #模拟单击搜索

    # 模拟单击微博文章
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/ul/li[3]/a').click()
    html = driver.page_source       #提取网页源码
    #获取文章子网页超链接
    list_urls = re.findall('<a href="(.*?)" target="_blank" suda-data="key=tblog_search_weibo&amp;value=seqid.*?<img src', html)

    urls = [] #保存子网页的超链接
    #爬取微博关键字文章第一页内容
    for url_i in list_urls:
        time.sleep(2)
        urls.append(url_i)
    print("爬取完成第 1 页文章内容")

    #爬取微博关键字第二页之后内容
    for i in range(2, page + 1):
        time.sleep(2)
        driver.find_element_by_class_name('next').click()  # 模拟单击下一页
        html = driver.page_source  # 提取子网页源码
        # 获取文章子网页超链接
        list_urls = re.findall('<a href="(.*?)" target="_blank" suda-data="key=tblog_search_weibo&amp;value=seqid.*?<img src', html)
        for url_j in list_urls:
            time.sleep(2)
            urls.append(url_j)
        print("爬取完成第 {} 页文章内容".format(i))

    for url_info in urls:
        time.sleep(2)
        # 因微博文章，个人非营业性账号发表的文章其网页会缺失'https:'前缀，
        # 出现无法爬取网页内容，通过判断添加'https:'
        if 'https:' not in url_info:
            url_info = 'https:' + url_info
            get_info(url_info,word)
        else:
            get_info(url_info,word)


def get_info(url_info,word):

    driver.get(url_info)
    driver.implicitly_wait(10)   # 隐式等待,显示等待搜索页面全部渲染完成
    url_html = driver.page_source  # 提取网页源码
    #文章发表账号
    author =re.findall('<em class="W_autocut">(.*?)</em>', url_html)
    #文章编辑时间
    edit_time = re.findall('<span class="time">(.*?)</span>', url_html)
    #文章阅读量
    num = re.findall('<span class="num">(.*?)</span>', url_html)

    # 文章标题
    titles = re.findall('<div class="title" node-type="articleTitle">(.*?)</div>', url_html)
    # 文章内容文本
    texts = re.findall('<p align="justify">(.*?)</p>|<span style="margin-top.*?>(.*?)</span>', url_html)
    texts_untreated_s = list(texts)  # 爬取但未经处理的数据
    text = []  # 只含有中文文本数据
    for i in texts_untreated_s:
        text_un_s = "".join(i)
        text_un = re.findall('[\u4e00-\u9fa5]+', text_un_s)  # 正则表达式筛选中文文本
        if text_un:  # 剔除空值
            text.append("".join(text_un))


    #文章账号个性签名
    signature = re.findall('<a href=".*?" target="_blank" class="S_txt1">(.*?)</a>', url_html)
    #文章转发数
    forwarding_num = re.findall('<span class="line S_line1" node-type="forward_btn_text">转发(.*?)</span>', url_html)
    #文章评论数
    comments_num = re.findall('<span class="line S_line1" node-type="comment_btn_text">评论(.*?)</span>', url_html)
    #文章点赞数
    likes_num = re.findall('<span node-type="like_status"><i class="W_icon icon_praised_b"></i> <em>(.*?)</em></span>', url_html)



    #"文章标题:""文章内容文本:""文章发表账号:" "文章编辑时间:""文章阅读量:"
    # "账号个性签名:""转发数:""评论数:""点赞数:"
    data = ["".join(titles), "".join(text),"".join(author),"".join(edit_time),
            "".join(num), "".join(signature),
            "".join(forwarding_num), "".join(comments_num),
            "".join(likes_num)
            ]
    data_cloud = ["".join(titles)+"".join(text)]#词云数据
    # 因部分微博文章是微博推广广告文章或主体为其他内容，
    # 因文章内又出现部分关联词而显示，但内容与关键字关联性不足，所以剔除爬取信息为空的数据
    for i in data:  #剔除爬取信息为空的数据
        if i.strip() != '':

            name = '微博{}文章数据'.format(word)
            with open(name+'.csv', 'a+', newline='', encoding='utf-8-sig') as file:  # 创建文件对象
                # 为文件对象构建 csv写入对象
                writer = csv.writer(file)
                writer.writerow(data)  # 添加数据

            with open(name+'.txt', 'a+') as f:
                f.write(data)
                f.close()

            #保存分类单独制作词云数据
            name1 = '微博{}文章词云数据.csv'.format(word)
            with open(name1, 'a+', newline='', encoding='utf-8-sig') as file:  # 创建文件对象
                # 为文件对象构建 csv写入对象
                writer = csv.writer(file)
                writer.writerow(data_cloud)  # 添加数据

            break
        else:
            print("此文章存在商业广告 或 内容与关键字关联性不足")
            break

#Jieba分词并统计词频
def word_jieba(word_name):
            # 设置pd的列长度
            pandas.set_option('max_colwidth', 500)
            # 载入csv数据
            name_w = '微博{}文章词云数据.csv'.format(word_name)
            rows = pandas.read_csv(name_w, encoding='gb18030', dtype=str)
            print(rows)
            strs = []
            # 对表格每一行进行遍历，然后分词
            for index, row in rows.iterrows():
                # 二维列表中行数据
                content = row[0]
                # 通过execl表格载入的每一行以textrank获取固定词性关键词
                words = jieba.analyse.textrank(content)
                # 将行数据中获取的关键词，以字典的形式加入到列表中
                for word in words:
                    strs.append({'word': word, 'count': 1})
            # 通过保存关键字的列表建立DataFrame
            dfstr = pandas.DataFrame(strs)
            # 词频统计，通过groupby函数从DataFrame中word的属性‘count’，求出总和
            dfword = dfstr.groupby('word')['count'].sum()
            #对Series的值进行前十降序排列
            print(dfword.sort_values(ascending=False)[0:10])
            # 保存为csv文件
            name = '微博{}文章词频.csv'.format(word_name)
            dfword.to_csv(name, encoding='utf-8')

#微博话题词云制作
def wordcloud():
    f = open('微博汉服文章数据.txt', encoding='GBK')  # 打开指定txt文件，编码为utf-8
    data = f.read()  # 读取文件内容
    res = jieba.lcut(data)  # 精确分词,变为列表
    result = ''.join(res)  # 把列表组合成字符串
    # color_mask = imread('五角星.jpg')                             #设定形状
    wc = WordCloud(font_path=r'C:\Windows\Fonts\simkai.ttf',  # windows内的字体文件
                   background_color='white',
                   width=1080,
                   height=960,
                   # mask = color_mask                              #给定词云形状
                   )
    wc.generate(result)  # 向WordCloud对象wc中加载文本
    wc.to_file('微博汉服词云.png')  # 将词云输出为图像文件
    plt.imshow(wc)
    plt.show()  # 显示图片

if __name__ == '__main__':

    # url = 'https://s.weibo.com/'
    # page = 11       # 新浪微博文章数据总共11页,所以爬取11页数据
    word = ['汉服', '汉服摄影', '汉服设计', '汉服星探', '汉服商家资讯', '传统文化', '文化自信', '汉服市场']
    # for w in word:
    #     time.sleep(5)
    #     get_selenium(url, page, w)
    # #
    # word1 = word[0]
    # word_jieba(word1)
    wordcloud()