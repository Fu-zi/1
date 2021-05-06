#-*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import jieba
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import jieba.analyse
import numpy as np
import matplotlib

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html',
    'Cookie': "_uuid=1DBA4F96-2E63-8488-DC25-B8623EFF40E773841infoc; buvid3=FE0D3174-E871-4A3E-877C-A4ED86E20523155831infoc; LIVE_BUVID=AUTO8515670521735348; sid=l765gx48; DedeUserID=33717177; DedeUserID__ckMd5=be4de02fd64f0e56; SESSDATA=cf65a5e0%2C1569644183%2Cc4de7381; bili_jct=1e8cdbb5755b4ecd0346761a121650f5; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(umY))|ukl~0J'ulY~uJm)kJ; UM_distinctid=16ce0e51cf0abc-02da63c2df0b4b-5373e62-1fa400-16ce0e51cf18d8; stardustpgcv=0606; im_notify_type_33717177=0; finger=b3372c5f; CURRENT_QUALITY=112; bp_t_offset_33717177=300203628285382610"

}
#获取存有弹幕信息数据xml文件网站的cid编号
def get_cid(av_id):
    # 向网页发起请求，并获取网页源码
    response = requests.get('https://www.bilibili.com/video/av'+av_id, headers=headers)
    #正则表达式获取cid码，
    cid = re.findall('cid=(.*?)&aid', response.text)[0]
    print(cid)
    get_info(cid)

#获取xml文件中的弹幕数据，并保存至本地
def get_info(cid):
    url = "https://comment.bilibili.com/{}.xml".format(cid)
    # 发送请求、以字节形式（二进制并返回解码为utf-8格式
    response = requests.get(url, headers=headers).content.decode('utf-8')
    #创建beautifulsoup对象，将请求之后的响应传入lxml解析器
    soup = BeautifulSoup(response, "lxml")
    #查找弹幕所在的d标签
    danmu = soup.find_all('d')
    contents = [i.text for i in danmu ]    #获取标签内的文本信息
    # 调用revise函数，剔除无用字符
    content = [revise(word) for word in contents]

    # 保存结果
    data = content
    # 把列表转换成DataFrame
    df = pd.DataFrame(data)

    #删除空字符串，替换为np.nan
    df.replace(to_replace=r'^\s*$', value=np.nan, regex=True, inplace=True)
    #删除包含的缺失值
    Df = df.dropna()
    #保存到本地
    Df .to_csv("bilibili_data.csv", encoding='utf-8-sig')

    # 词云制作
    wordcloud()
    #jieba分词，输出文本高频词
    word_jieba(Df)


#调整数据格式与内容，剔除无用字符
def revise(str):
    return str.replace(" ", "").replace("\n", "").replace("\t", "").replace("？", "")\
        .replace("《", "").replace("》", "").\
        replace("6", "").replace("2", "").replace("3", "").replace("哈", "").strip()

#b站弹幕词云制作
def wordcloud():
    # 对来自外部文件的文本进行中文分词，得到string
    file = open('bilibili_data.csv', encoding='utf-8')
    txt = file.read()  # 读取文件内容
    txt_list = jieba.lcut(txt)    #精确分词,变为列表
    strings = " ".join(txt_list)  # 把列表组合成字符串

    # 创建停用词list
    stopwords = [line.strip()for line in
                 open('stop_words.txt', 'r', encoding='utf-8').readlines()]

    w = WordCloud(width=1080,
                  height=960,
                  background_color='black',  #设置背景颜色
                  font_path='msyh.ttc',  # 设置为楷体 windows内的字体文件
                  stopwords=stopwords,  # 设置停用词
                  contour_width=5  #轮廓宽度
                  )

    # WordCloud词云对象w中输入文字加载文本
    w.generate(strings)
    # 将词云图片导出到当前文件夹
    w.to_file(r"b站词云.png")  # 将词云输出为图像文件
    plt.imshow(w)  # 看图
    plt.show()  # 显示图片


#Jieba分词并统计词频
def word_jieba(Df):
    # 设置pd的列长度
    pd.set_option('max_colwidth', 500)
    # 载入csv数据
    strs = []
    # 对Df的dataframe对象每一行进行遍历，然后分词
    for index, row in Df.iterrows():
        # 二维列表中行数据
        content = row[0]
        # 通过execl表格载入的每一行以textrank获取固定词性关键词
        words = jieba.analyse.textrank(content)
        # 将行数据中获取的关键词，以字典的形式加入到列表中
        for word in words:
            strs.append({'word': word, 'count': 1})
    # 通过保存关键字的列表建立DataFrame
    dfstr = pd.DataFrame(strs)
    # 词频统计，通过groupby函数从DataFrame中word的属性‘count’，求出总和
    dfword = dfstr.groupby('word')['count'].sum()
    # 创建停用词list
    stopwords = [line.strip()for line in
                 open('stop_words.txt', 'r', encoding='utf-8').readlines()]
    #删除dfword中包含停用词的series值
    for word in dfword.index:
        if word in stopwords:  #当含有停用词
            del dfword[word]   # 删除了某个索引后，对应的值也同时删除了

    # 对Series的值进行前十降序排列，并进行输出
    data = dfword.sort_values(ascending=False)[0:10]
    print(data)
    # 保存为csv文件
    data.to_csv('b站词频.csv', encoding='utf-8', header=True)
    index = data.index.tolist()                       #Series的键转换为列表
    values = data.values.tolist()                 #Series的值转换为列表
    #饼状图制作
    pie_chart(index, values)
    #柱状图制作
    histogram(index, values)

# b站弹幕词频饼状图制作
def pie_chart(index,values):
    # 使用matplotlib的字体管理器指定字体文件
    font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)

    # 解决汉字乱码问题
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用指定的汉字字体类型（此处为黑体）

    indic = []
    # 将数据最大的突出显示
    for value in values:
        if value == max(values):
            indic.append(0.1)
        else:
            indic.append(0)
    plt.pie(
        x=values,   #数据
        labels=index,   #标签
        startangle=90,  #开始绘图的角度
        shadow=True,    #是否显示阴影
        explode=tuple(indic),  # 突出的部分, tuple方法用于将列表转化为元组
        autopct='%1.1f%%'  # 数据标签	是数字1，不是l
    )
    plt.title(u'饼图示例—各弹幕高频词比例', FontProperties=font)
    # 保存图列至本地
    plt.savefig('饼图图.png', dpi=300)
    # 显示图片
    plt.show()


#b站弹幕词频条形图制作
def histogram(index,values):
    # 将全局的字体设置为黑体
    matplotlib.rcParams['font.family'] = 'SimHei'
    # 数据样本数
    N = 10

    x = np.arange(N)    #有终点和起点的固定步长的排列,即直线图中的X轴
    # 绘图 x x轴， height 高度, 默认：color="blue", width=0.3
    plt.bar(x, height=values, width=0.3, label="弹幕出现数量: 个", tick_label=index, color="pink")
    # 添加数据标签
    for a, b in zip(x, values):
        plt.text(a, b, '%.2f' % b, ha='center', va='bottom', fontsize=10)

    plt.title('条形图示例—弹幕高频词量')
    # 添加图例
    plt.legend()
    # 保存图列至本地
    plt.savefig('条形图.png', dpi=300)
    # 展示图形
    plt.show()


if __name__ =="__main__":
    av_id = '456098516'
    get_cid(av_id)
