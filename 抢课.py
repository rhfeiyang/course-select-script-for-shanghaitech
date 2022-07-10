import os
import sys
from copy import deepcopy
from time import sleep, mktime, strptime, strftime, time, localtime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

#IDE运行须注释 shanghaitechrh
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(sys._MEIPASS, 'cacert.pem')


def waitbegin():
    zero_time = mktime(strptime(strftime('%Y年%m月%d日'), '%Y年%m月%d日'))
    while 1:
        for h in on_time:
            on = zero_time + h * 60 * 60
            if time() < on + 60:
                while 1:
                    if (on - time()) > 120:
                        print("等待中，下次开始时间:", h, "时  现在时间:", strftime('%m月%d日%H:%M:%S'))
                        sleep(80)
                    elif (on - time()) <= 40:
                        print("即将开始：", strftime('%m月%d日%H:%M:%S', localtime(on)))
                        return on
                    else:
                        sleep(4)
            else:
                continue


def getDriver(option):
    # if getattr(sys,'frozen',False):
    #     path=os.path.join(sys._MEIPASS,"chromedriver.exe")
    #     return webdriver.Chrome(options=option, executable_path=path)
    # else:
    #     return webdriver.Chrome(options=option, executable_path='./chromedriver.exe')
    return webdriver.Chrome(options=option, service=ChromeService(ChromeDriverManager().install()))


def login(option, name, pwd, try_login):
    driver = getDriver(option)
    driver.get("https://egate.shanghaitech.edu.cn/new/index.html")
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.ID, 'ampLoginBtn')).click()
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.NAME, "username")).send_keys(name)
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH, '//*[@id="password"]')).send_keys(pwd)
    WebDriverWait(driver, timeout=5).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="casLoginForm"]/p[4]/button')).click()
    try:
        WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.XPATH,
                                     '//*[@id="ampTabContentItem0"]/div[3]/pc-card-html-5041679979648433-01/amp-w-frame/div/div[2]/table[1]/tbody/tr[1]/td[1]/a/img'))
        if try_login:
            print("登录成功")
            driver.quit()
            return True
        else:
            return driver
    except TimeoutException:
        if try_login:
            print("账号密码错误或网络错误，请重试")
            driver.quit()
            return False
        else:
            return driver


def main():
    classes = []
    print("请输入课程序号，一行一个，如：CHEM1300.01，输入-1结束")
    c = input()
    while c != "-1":
        classes.append(c)
        c = input()
    print("课程序号为：", classes)

    option = webdriver.ChromeOptions()
    show_head = input("是否显示浏览器(y/n)")
    if show_head != "Y" and show_head != "y":
        if show_head == "N" or show_head == "n":
            option.add_argument('--headless')
        else:
            print("输入错误，默认不显示")
            option.add_argument('--headless')
    option.add_argument("--window-size=1920,1080")
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument("start-maximized")  # https://stackoverflow.com/ab/26283818/1689770
    option.add_argument("enable-automation")  # https://stackoverflow.com/ay/43840128/1689770
    option.add_argument("--no-sandbox")  # https://stackoverflow.com/ar/50725918/1689770
    option.add_argument("--disable-infobars")  # https://stackoverflow.com/ah/43840128/1689770
    option.add_argument("--disable-dev-shm-usage")  # https://stackoverflow.com/a/50725918/1689770
    option.add_argument("--disable-browser-side-navigation")  # https://stackoverflow.com/a/49123152/1689770
    option.add_argument(
        "--disable-gpu")  # https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
    username = input("请输入egate账号：")
    pwd = input("请输入密码：")
    while not login(option, username, pwd, True):
        username = input("请输入egate账号：")
        pwd = input("请输入密码：")
    while classes:
        on = waitbegin()
        print("课程列表：", classes)
        driver = login(option, username, pwd, False)
        WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.XPATH,
                                     '//*[@id="ampTabContentItem0"]/div[3]/pc-card-html-5041679979648433-01/amp-w-frame/div/div[2]/table[1]/tbody/tr[1]/td[1]/a/img')).click()
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="MLeft"]/div/ul/li[1]/a')).click()
        WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="MLeft"]/div/table[2]/tbody/tr[5]/td[1]/div[2]/a')).click()
        WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.LINK_TEXT,"进入选课>>>>")).click()
        driver.switch_to.window(driver.window_handles[-1])
        while time() <= on + 90:
        #while 1:
            if not classes: break
            bac_classes = deepcopy(classes)
            for cla in bac_classes:
                try:
                    WebDriverWait(driver, timeout=3).until(
                        lambda d: d.find_element(By.NAME, "electableLesson.no")).clear()
                    WebDriverWait(driver, timeout=3).until(
                        lambda d: d.find_element(By.NAME, "electableLesson.no")).send_keys(cla + Keys.ENTER)
                    try:
                        driver.find_element(By.LINK_TEXT, '选课').click()
                    except NoSuchElementException:
                        print(cla + '已选')
                        classes.remove(cla)
                        continue
                except (UnexpectedAlertPresentException, TimeoutException):
                    print(cla, "网络错误，重试")
                    driver.refresh()
                    sleep(0.5)
                    continue
                alert = driver.switch_to.alert
                print(cla, alert.text)
                alert.accept()
                driver.refresh()
                sleep(0.5)
        print(strftime('%m月%d日%H:%M:%S'), "未选上的课：", classes)
        driver.quit()
    print("任务完成")


on_time = [8, 10, 12, 16, 20, 24]

main()
