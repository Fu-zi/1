import requests
import time
import re
import pymysql

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

conn = pymysql.connect(host='localhost', user='root', password='123', db='qianpeng', port=3306, charset='utf8')  # 连接mysql
cursor = conn.cursor()  # 创建游标对象

#调整输出格式
def textStrip(s):
    return str("".join(s).replace("-", "").replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "").strip())

#判断列表是否为空,(空格、制表符、换行符)，
def judge (list):
    if ''.join(list).isspace():
        list = '无'
    else:
        return list
    return list

#获取子页面网站地址
def get_info(url):
    print(url)
    datas = []
    response = requests.get(url, headers=headers).text
    titles = re.findall('<a class="title" target="_blank" href=".*?">(.*?)</a>', response)#标题
    contents = re.findall('class="abstract">.*?\n      (.*?)</p>', response, re.S)#文章内容
# 观看数
    reads = re.findall('<i class="iconfont ic-list-read"></i> (.*?)\n</a>', response, re.S)
#评论数
    comments = re.findall('<i class="iconfont ic-list-comments"></i> (.*?)\n</a>', response, re.S)
#喜欢人数
    loves = re.findall('<span><i class="iconfont ic-list-like"></i> (.*?)</span>', response)
#打赏人数
    rewards = re.findall('<span><i class="iconfont ic-list-money"></i> (.*?)</span>', response)
#发表时间
    timels = re.findall('<span class="time" data-shared-at="(.*?)T', response, re.S)
    for title, contentt, read, comment, love, reward, timel in \
         zip(titles, contents, reads, comments, loves, rewards, timels):
        print(type(title))
        content = textStrip(''.join(judge(contentt)))
        data = {
        '标题': title,
        '文章内容': content,
        '观看数': read,
        '评论数': comment,
        '喜欢人数': love,
        '打赏人数': reward,
        '发表时间': timel
    }
        print(data)

        cursor.execute("insert into jianshu_hot(标题,文章内容,观看数,评论数,喜欢人数,打赏人数,发表时间)"
                       "values(%s,%s,%s,%s,%s,%s,%s)",
            (title, str(content), str(read),
             str(comment), str(love), str(reward), str(timel)))


if __name__ =='__main__':

    urls = ['https://www.jianshu.com/u/9104ebf5e177?order_by=top&page={}'.format(str(i))for i in range(1, 2)]# 爬取第一页25部电影
    for url in urls:
        get_info(url)
        time.sleep(2)

    conn.commit()  # 提交数据
    cursor.close() # 关闭游标
    conn.close()# 关闭数据库连接



