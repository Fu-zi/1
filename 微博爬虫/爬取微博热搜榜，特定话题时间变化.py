import requests
import re
import time
import matplotlib.pyplot as plt
import numpy as np

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

def textStrip(s):
    return ''.join(s).replace(" ", "").replace("\n", "").replace("\t", "").strip()

def getHTMLpage(url,title,name1,name2):
    response = requests.get(url, headers=header)


    text = response.text
    result_re = re.findall(r'\d</td>.*\S'+title+'</a><span>\d*', textStrip(text))
    ranking = re.sub(r'</?(.+?)>'+title+'.*</?(.+?)>\d*',"", textStrip(result_re))
    num = re.sub(r'\d*</?(.+?)>'+title+'.*</?(.+?)>',"", textStrip(result_re))

    with open(name1+".txt", 'a+') as f:
        f.write(ranking)
        f.close()

    with open(name2+".txt", 'a+') as f:
        f.write(num)
        f.close()




def Drawing(name1,name2):
    plt.figure(1)
    ranking = np.loadtxt(name1+"变化图.txt")
    time = [0, 10, 20, 30, 40, 50, 60]
    x = range(len(time))
    y1 = ranking
    plt.plot(x,y1, label='Change line', marker='*')
    plt.legend()  # 让图例生效
    plt.xticks(x, time, rotation=45)
    plt.xlabel("time")  # X轴标签
    plt.ylabel('Variety')  # Y轴标签
    plt.title('Change chart')  # 标题



    plt.figure(2)
    ranking = np.loadtxt(name2 + "变化图.txt")
    time = [0, 10, 20, 30, 40, 50, 60]
    x = range(len(time))
    y2 = ranking
    plt.plot(x, y2, label='Change line', marker='*')
    plt.legend()  # 让图例生效
    plt.xticks(x, time, rotation=45)
    plt.xlabel("time")  # X轴标签
    plt.ylabel('Variety')  # Y轴标签
    plt.title('Change chart')  # 标题

    plt.legend()
    plt.show()

    plt.savefig(name2+'变化图.png',name1 + '变化图.png')

if __name__ == '__main__':
    url = 'https://s.weibo.com/top/summary'
    title = '111'
    name1 = '微博热搜榜排名'
    name2 = '微博热搜榜搜索量'

    for i in range(0, 7):
        times = i*10
        print("第{}分钟数据已获取".format(times))
        getHTMLpage(url,title,name1,name2)
        time.sleep(600)

    Drawing(name1,name2)
