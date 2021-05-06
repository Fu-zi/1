
import requests
from bs4 import BeautifulSoup
import re
import time
import os
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

def getHTML(url):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    HTML_li = soup.find("ul", class_="house-list")

    num =0
    for x in HTML_li:
        time.sleep(1)
        html = str(x)
        soup = BeautifulSoup(html, 'html.parser')
        num = num + 1
        result_href = soup.find('a', 'href')
        url = result_href
        print(url)
        print("1")




def specificalHTML(url):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')

    html = soup.find_all('div', class_="switch_list")[0].text
    html11 = soup.find_all('div', class_="img_wrap")[0]
    print("1")

    print(html)
    # url = url.decode('utf-8')
    # reg = r'src="(.+?\.jpg)" '
    # imgre = re.compile(reg)
    # imglist = re.findall(imgre, url)
    # print(imglist)






    # try:
    #     url = ''  # 图片地址
    #     root = "E:/pic/"
    #     path = root + url.split("/")[-1]
    #     if not os.path.exists(root):  # 目录不存在创建目录
    #         os.mkdir(root)
    #     if not os.path.exists(path):  # 文件不存在则下载
    #         r = requests.get(url)
    #         f = open(path, "wb")
    #         f.write(r.content)
    #         f.close()
    #         print("文件下载成功")
    #     else:
    #         print("文件已经存在")
    # except:
    #     print("获取失败")


def main():
    pagenum = 2
    for i in range(1, pagenum):
        url = 'https://gz.58.com/chuzu/pn{}'.format(i)
        print('第{}页抓取中'.format(i))
        time.sleep(1)
        getHTML(url)


if __name__ == '__main__':
    main()
