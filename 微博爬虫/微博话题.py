from wordcloud import WordCloud     #导入子包，节约资源
import matplotlib.pyplot as plt     #下载matplotlib包
import requests
import re
import jieba
import time
import asyncio
import csv
import pandas
import imageio as imageio   #加载图片

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
async def get_title(url):
    time.sleep(1)
    response = requests.get(url, headers=header).text
    title = re.findall('class="name" suda-data="key=tblog_s.*?_name">#(.*?)#</a>', response)
    print(title)
    with open('微博词云.txt', 'a+') as f:
        f.write(" ".join(title))
        f.close()
    with open('微博话题.csv', 'a+', newline='', encoding='utf-8-sig') as file:  # 创建文件对象
        # 为文件对象构建 csv写入对象
        writer = csv.writer(file)
        writer.writerow(" ".join(title))  # 添加数据

 #中文jieba分词
#Jieba分词并统计词频
def word_jieba():
            # 设置pd的列长度
            pandas.set_option('max_colwidth', 500)
            # 载入csv数据
            rows = pandas.read_csv('微博话题数据', encoding='gb18030', dtype=str)
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
            dfword.to_csv('微博话题词频数据.csv', encoding='utf-8')

#微博话题词云制作
def wordcloud():
    f = open('微博话题.txt', encoding='GBK')  # 打开指定txt文件，编码为utf-8
    data = f.read()  # 读取文件内容
    res = jieba.lcut(data)  # 精确分词,变为列表
    result = ''.join(res)  # 把列表组合成字符串
    # color_mask = imageio.imread('五角星.jpg')                             #设定形状
    wc = WordCloud(font_path=r'C:\Windows\Fonts\simkai.ttf',
                   background_color='white',
                   width=1080,
                   height=960,
                   # mask = color_mask                              #给定词云形状
                   )
    wc.generate(result)  # 向WordCloud对象wc中加载文本
    wc.to_file('微博词云.png')  # 将词云输出为图像文件
    plt.imshow(wc)
    plt.show()  # 显示图片

# 异步处理网页，获取name和description
async def download(url):
        try:
            await get_title(url)
        except Exception as err:
            print(err)

if __name__ == '__main__':
    page = 50
    word = ['汉服']
    # for w in word:
    #     urls = ['https://s.weibo.com/topic?q={}'
    #             '&pagetype=topic&topic=1&Refer=article_topic&page={}'.format(word, str(i))for i in range(0, page+1)]
    #     for url in urls:
    #         # 利用asyncio模块进行异步IO处理
    #         loop = asyncio.get_event_loop()
    #         tasks = [asyncio.ensure_future(download(url))]
    #         tasks = asyncio.gather(*tasks)
    #         loop.run_until_complete(tasks)
    # word_jieba() #中文jieba分词
    wordcloud()  #微博话题词云制作

