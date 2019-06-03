from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import cv2
import numpy as np
from io import BytesIO
import time, requests
import random
from chaojiying import Chaojiying_Client

"""
网易文字点选验证码破解
"""


class YidunV2(object):

    def __init__(self):
        self.url = 'http://dun.163.com/trial/picture-click'
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_option)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def open(self):
        self.driver.get(self.url)

    def start_select(self):
        res = self.get_position()
        print(res)
        coordinates = res["pic_str"].split("|")
        print(coordinates)
        yidun_img = self.driver.find_element_by_class_name("yidun_bg-img")

        ActionChains(self.driver).move_to_element_with_offset(yidun_img, xoffset=int(coordinates[0].split(',')[0]),
                                                              yoffset=int(coordinates[0].split(',')[1])).click().perform()
        time.sleep(random.randint(500, 1000) / 300)
        x1 = int(coordinates[1].split(",")[0]) - int(coordinates[0].split(",")[0])
        y1 = int(coordinates[1].split(",")[1]) - int(coordinates[0].split(",")[1])
        x1_tracks = self.get_tracks(x1)
        y1_tracks = self.get_tracks(y1)
        x_tracks, y_tracks = self._average(x1_tracks, y1_tracks)
        print(x1_tracks, y1_tracks)
        # 2次for循环代表在点击的基础上继续移动鼠标，这样识别率较高
        for x, y in zip(x_tracks, y_tracks):
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=y).perform()
            time.sleep(random.randint(50, 100) / 2000)
        ActionChains(self.driver).click().perform()
        time.sleep(1)
        x2 = int(coordinates[2].split(",")[0]) - int(coordinates[1].split(",")[0])
        y2 = int(coordinates[2].split(",")[1]) - int(coordinates[1].split(",")[1])
        x2_tracks = self.get_tracks(x2)
        y2_tracks = self.get_tracks(y2)
        x2_tracks, y2_tracks = self._average(x2_tracks, y2_tracks)
        print(x2_tracks, y2_tracks)
        for m, n in zip(x2_tracks, y2_tracks):
            ActionChains(self.driver).move_by_offset(xoffset=m, yoffset=n).perform()
            time.sleep(random.randint(50, 100) / 2000)
        ActionChains(self.driver).click().perform()
        time.sleep(2)

        try:
            self.wait.until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[@class='yidun_tips__text yidun-fallback__tip']"), '验证成功'))
            print("认证成功")
            self.driver.close()
        except:
            print("认证失败")
            self.start_select()


    def get_captcha(self):
        """获取验证码并保存到本地"""
        yidun_btn = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_tips')))
        ActionChains(self.driver).move_to_element(yidun_btn).perform()
        time.sleep(0.5)
        self.driver.save_screenshot("screenshot.png")
        time.sleep(0.5)
        image1 = Image.open("screenshot.png")
        image2 = image1.crop((928, 840, 1567, 1258))
        image2.save('screenshot.png')
        image2 = Image.open("screenshot.png")
        image3 = image2.resize((320, 205))
        image3.save("screenshot.png")

    def get_position(self):
        """通过超级鹰得到坐标"""
        self.get_captcha()
        time.sleep(0.2)
        chaojiying = Chaojiying_Client('vivi9310', 'bulibuqi1314', '899845')
        im = open('screenshot.png', 'rb').read()
        return chaojiying.PostPic(im, 9103)

    def get_tracks(self, distance):
        """
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        """
        print(distance)
        if distance < 0:
            distance = -distance
            tracks = self._get_tracks(distance)
            tracks = [-i for i in tracks]
            return tracks + [1]
        else:
            return self._get_tracks(distance) + [1]

    def _get_tracks(self, distance):
        v = 0
        t = 0.2
        tracks = []
        current = 0
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                a = 3
            else:
                a = -4
            v0 = v
            s = v0 * t + 0.5 * a * (t ** 2)
            current += s
            tracks.append(round(s))
            v = v0 + a * t
        return tracks + [1]

    def _average(self, x, y):
        if len(x) > len(y):
            for i in range(len(x) - len(y)):
                y.append(0)
        elif len(x) < len(y):
            for i in range(len(y) - len(x)):
                x.append(0)
        return x, y


if __name__ == '__main__':
    cs = YidunV2()
    cs.open()
    cs.start_select()
