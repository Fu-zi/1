import requests
import time
import re
import pymysql

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

conn = pymysql.connect(host='localhost', user='root', password='123', db='qianpeng', port=3306, charset='utf8')  # 连接mysql
cursor = conn.cursor()  # 创建游标对象

#获取子页面网站地址
def get_url(url):
    html = requests.get(url, headers=headers)
    links = re.findall('<a href=\"(.*?)\" class="">', html.text)

    for link in links:
        time.sleep(2)
        get_info(link)



def  get_info(link):#get-info 获取详细信息

    # 电影名称、导演、主演、类型、制片国家、上映时间、片长和上映时间
    response = requests.get(link, headers=headers).text

    name = re.findall('<span property="v:itemreviewed">(.*?)</span>', response)[0]  # 电影名称
    dirctor = re.findall('</span>:.*?<a href=.*? rel="v:directedBy">(.*?)</a></span>', response)[0]  # 导演
    actor_list = re.findall('<a href=.*? rel="v:starring">(.*?)</a>', response)[0:30]  # 主演
    actor = ' '.join(actor_list)
    Type_list = re.findall('<span property="v:genre">(.*?)</span>', response)  # 类型
    Type = ''.join(Type_list)
    #制片国家
    produ_country = re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>', response, re.S)[0]

    # 上映时间
    release_time = re.findall('<span property="v:initialReleaseDate" content=.*?>(.*?)</span>', response)[0]
    # 片长
    movice_time = re.findall('<span property="v:runtime" content=.*?>(.*?)</span>', response)[0]
    # 评分
    score = re.findall('<strong class="ll rating_num" property="v:average">(.*?)</strong>', response)[0]
    data = {
        '电影名称': name,
        '导演': dirctor,
        '主演': actor,
        '类型': Type,
        '制片国家': produ_country,
        '上映时间': release_time,
        '片长': movice_time,
        '评分': score
    }
    print(data)


    cursor.execute("insert into movietop(电影名称,导演,主演,类型,制片国家,上映时间,片长,评分)"
                   "values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   (str(name), str(dirctor),
                    str(actor), str(Type), str(produ_country), str(release_time),
                    str(movice_time), str(score)
                    ))

if __name__ =='__main__':
    urls = ['https://movie.douban.com/top250?start={}&filter='.format(str(i))for i in range(0, 25, 25)]# 爬取第一页25部电影
    for url in urls:
        get_url(url)
        time.sleep(2)

    conn.commit()  # 提交数据
    cursor.close() # 关闭游标
    conn.close()# 关闭数据库连接