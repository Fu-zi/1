
from selenium import webdriver
import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request
import cv2
import numpy as np

chromedriver_path = r"C:\Program Files\Python37\Scripts\chromedriver.exe"  # 谷歌chromedriver完整路径
options = webdriver.ChromeOptions()  # 配置 chrome 启动属性
options.add_experimental_option("excludeSwitches",['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
driver=webdriver.Chrome(executable_path=chromedriver_path,options=options)
wait=WebDriverWait(driver,10) #超时时长为10s

def login(username, password):
    driver.get("https://passport.jd.com/new/login.aspx")
    time.sleep(5)
    driver.find_element_by_link_text("账户登录").click()
    driver.find_element_by_name("loginname").send_keys(username)
    driver.find_element_by_name("nloginpwd").send_keys(password)
    time.sleep(5)
    driver.find_element_by_id("loginsubmit").click()
    # getpic()
    time.sleep(3)
    driver.get("https://cart.jd.com/cart.action")
    time.sleep(3)
    # webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
    now = datetime.datetime.now()
    #now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print(now.strftime('%Y-%m-%d %H:%M:%S'))


def getpic():
    #定位验证图片的大图，获取src标签地址
    bigimg = driver.find_element_by_xpath(r'//div/div[@class="JDJRV-bigimg"]/img').get_attribute("src")
    #定位验证图片的小图，获取src标签地址
    smallimg = driver.find_element_by_xpath(r'//div/div[@class="JDJRV-smallimg"]/img').get_attribute("src")
    # print(bigimg)
    # 背景大图命名
    backimg = "backimg.png"
    # 滑块命名
    slideimg = "slideimg.png"
    # 下载背景大图保存到本地
    urllib.request.urlretrieve(str(bigimg), backimg)
    # 下载滑块保存到本地
    urllib.request.urlretrieve(str(smallimg), slideimg)
    # 获取图片并灰度化
    block = cv2.imread(slideimg, 0)
    template = cv2.imread(backimg, 0)
    # 二值化后的图片名称
    blockName = "block.jpg"
    templateName = "template.jpg"
    # 将二值化后的图片进行保存
    cv2.imwrite(blockName, block)
    cv2.imwrite(templateName, template)
    block = cv2.imread(blockName)
    block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
    block = abs(255 - block)
    cv2.imwrite(blockName, block)
    block = cv2.imread(blockName)
    template = cv2.imread(templateName)
    # 获取偏移量
    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED) # 查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
    x, y = np.unravel_index(result.argmax(), result.shape)
    # print("x方向的偏移", int(y * 0.4 + 18), 'x:', x, 'y:', y)
    x1 = int(y*0.98)
    # 获取滑块
    element = driver.find_element_by_xpath(r'//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]')
    ActionChains(driver).click_and_hold(on_element=element).perform()
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=x1, yoffset=0).perform()
    print("登录成功")
    ActionChains(driver).release(on_element=element).perform()
    time.sleep(3)


def buy_on_time(buytime):
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    #关闭浏览器左上角的通知提示
    options.add_experimental_option('prefs', prefs)

    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if now >= buytime:
            element_area = driver.find_element_by_class_name('btn-area').click()
            driver.execute_script("arguments[0].click();", element_area)

            # print(driver.find_element_by_class_name('checkout-submit').click())
            element_submit = driver.find_element_by_class_name('checkout-submit').click()
            driver.execute_script("arguments[0].click();", element_submit)
            print(now)
            print('购买成功')
        time.sleep(0.5)

if __name__ == "__main__":
    login('18520992236', 'v5876666')
    print("账号登录成功")
    buy_on_time('2020-09-07 11:02:00')
