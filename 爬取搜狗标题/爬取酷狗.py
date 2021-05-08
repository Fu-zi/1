print(201806140055,'钱鹏  大数据1802')
import requests
from bs4 import BeautifulSoup
import time

def specific_data(url):  # 定义获取信息的函数
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > a')
    times = soup.select('span.pc_temp_tips_r > span')
    for rank, title, time in zip(ranks, titles, times):
        data = {
            '排名': rank.get_text().strip(),  # 歌曲序号
            '歌手': title.get_text().split('-')[0],  # 歌手名称
            '歌曲': title.get_text().split('-')[1],  # 歌曲名称
            '播放时间': time.get_text().strip()  # 歌曲时长
        }
        print(data)

if __name__ == '__main__':
    # 加入请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 QIHU 360EE'}
    # 构建多页url，每个网页有22条，500条结果需要23组
    urls = ['https://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(str(i))
            for i in range(1, 24)]

    for url in urls:
        specific_data(url)
        time.sleep(1)#设置时间反爬虫