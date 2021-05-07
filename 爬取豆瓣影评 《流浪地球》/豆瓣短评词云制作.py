import pandas as pd
import re


# 数据预处理
data = pd.read_csv('douban.csv', encoding='utf-8')
data.columns
data['入会时间']=data['入会时间'].apply(lambda x: re.sub('加入','',str(x)))
data['短评正文']=data['短评正文'].apply(lambda x: re.sub('\n','', x))

# 短片的整体的词云展示
# （1）分词：将句子切分为一个词或词组
import jieba
# jieba.lcut('今天我来广州商学院上课')
# jieba.lcut_for_search('今天我来广州商学院上课')
data_cut = data['短评正文'].apply(jieba.lcut)



# （2）去除停用词
with open('./stoplist.txt', 'r',encoding='utf-8') as f:
    stop = f.read()
stop = stop.split()
# 将data_cut中去除在stop列表中的出现的那些词
data_after=data_cut.apply(lambda x: [i for i in x if i not in stop]) # 去除停用词后


# （3）词频统计
from tkinter import _flatten
word_count = pd.Series(_flatten(list(data_after))).value_counts()


# 绘制词云
from wordcloud import WordCloud
import matplotlib.pyplot as plt
back = plt.imread('./aixin.jpg')    #设置词云图的背景图
wc = WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',mask=back,background_color='white')  #设置词云参数
wc2 = wc.fit_words(word_count)  # 传入词频信息
plt.imshow(wc2)
plt.show()


# 好评与差评的词云图展示
index = data['评分'] > 30 # 评分在30分以上的短评正文数据
data = data['短评正文']
good_data = data.loc[index, '短评正文'] # 好评数据
bad_data = data.loc[-index, '短评正文'] # 差评数据


def my_cloud(data, stop):
    data_cut = data.apply(jieba.lcut)
    data_after = data_cut.apply(lambda x: [i for i in x if i not in stop])  # 去除停用词后
    word_count = pd.Series(_flatten(list(data_after))).value_counts()
    wc = WordCloud(font_path='C:/Windows/Fonts/simhei.ttf', mask=back, background_color='white')  # 设置词云参数
    wc2 = wc.fit_words(word_count)  # 传入词频信息
    plt.imshow(wc2)
    plt.show()
    return word_count



# 好评词云的展示
my_cloud(good_data, stop)
# 差评词云的展示
my_cloud(bad_data, stop)



