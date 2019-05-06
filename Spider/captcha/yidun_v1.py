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

# 网易滑动验证码破解：https://www.jianshu.com/p/f12679a63b8d

class CrackSlider():
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """

    def __init__(self):
        self.url = 'http://dun.163.com/trial/jigsaw'
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_option)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.zoom = 1

    def open(self):
        self.driver.get(self.url)

    def start_slider(self):
        target = 'target.jpg'
        template = 'template.png'
        cs.get_pic()
        distance = cs.match(target, template)
        tracks = cs.get_tracks((distance + 15) * cs.zoom)  # 对位移的缩放计算
        cs.crack_slider1(tracks)

        # 判断是否验证成功
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun--success')))
        except TimeoutException:
            print("again times")
            # 失败后递归执行拖动
            self.start_slider()
        else:
            # 刷新，一直递归拖动，查看准确率
            self.driver.refresh()
            self.start_slider()

    def get_pic(self):
        time.sleep(2)
        target = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        template = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_jigsaw')))
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save('target.jpg')
        template_img.save('template.png')
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        self.zoom = 320 / int(size_loc[0])

    def get_tracks(self, distance):
        print(distance)
        distance += 20
        v = 0
        t = 0.1
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5  # 减速阀值
        while current < distance:
            if current < mid:
                a = 2  # 加速度为+2
            else:
                a = -3  # 加速度-3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -0.5]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    def match(self, target, template):
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        w, h = template.shape[::-1]
        print(w, h)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        run = 1

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            print("threshold: ", threshold)
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            print("loc[1]: ", len(loc[1]))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                return loc[1][0]
            elif len(loc[1]) < 1:
                R -= (R - L) / 2

    def crack_slider1(self, tracks):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(self.driver).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        ActionChains(self.driver).move_by_offset(xoffset=-4, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=2, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).move_by_offset(xoffset=2, yoffset=0).perform()
        time.sleep(0.5)

        ActionChains(self.driver).release().perform()

    def crack_slider2(self, distance):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(self.driver).click_and_hold(slider).perform()

        time.sleep(0.5)
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10, 50) / 100)

        ActionChains(self.driver).move_by_offset(distance, 0).perform()
        ActionChains(self.driver).release().perform()


if __name__ == '__main__':
    cs = CrackSlider()
    cs.open()
    cs.start_slider()
