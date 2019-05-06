import random
import time, re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import requests
from io import BytesIO


class Gsxt(object):
    def __init__(self):
        chrome_option = webdriver.ChromeOptions()
        # chrome_option._arguments = ['disable-infobars']
        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_option)
        self.driver.set_window_size(1440, 900)

    def visit_index(self):
        self.driver.get("https://id.163yun.com/register")
        time.sleep(10)
        # element = self.driver.find_element_by_id("keyword")
        # element = self.driver.find_element_by_xpath('//input[@id="keyword"]')
        # element.clear()
        # element.send_keys("微信")


        element = self.driver.find_element_by_xpath('//input[@id="gover_search_key"]')
        element.click()
        element.send_keys("当事人:刘鑫")

        time.sleep(5)

        # ele_btn = self.driver.find_element_by_xpath('//button[@id="btn_query"]')
        # ele_btn.click()
        # time.sleep(10)

        ele_btn = self.driver.find_element_by_xpath('//button[@class="head_search_btn"]')
        ele_btn.click()
        time.sleep(10)

        # class_name = "geetest_canvas_fullbg"
        # getImgJS = 'return document.getElementByClassName("' + class_name + '").toDataURL("image/png");'
        # bg_img = self.driver.execute_script(getImgJS)
        # bg_img = bg_img[bg_img.find(',') + 1:]
        # print(bg_img)
        #
        # class_name = "geetest_canvas_slice"
        # getImgJS = 'return document.getElementByClassName("' + class_name + '").toDataURL("image/png");'
        # bg_img = self.driver.execute_script(getImgJS)
        # bg_img = bg_img[bg_img.find(',') + 1:]
        # print(bg_img)


        # WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="js-register"]')))
        # reg_element = self.driver.find_element_by_xpath('//*[@class="js-register"]')
        # reg_element.click()
        #
        # WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_slider_knob gt_show"]')))
        #
        # # 进入模拟拖动流程
        # self.analog_drag()


if __name__ == "__main__":
    g = Gsxt()
    g.visit_index()
