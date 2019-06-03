from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from lxml import etree
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "accept-encoding": "gzip, deflate, br",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9",
    "authority": "mail.qq.com",
    "method": "GET",
    "path": "/cgi-bin/frame_html?sid=XTL_K7bFBfwmIDBs&r=03efc0df44c68703d1d1fbbcb017bd52",
    "scheme": "https",
    "cache-control": "max-age=0",
    "referer": "https://mail.qq.com/",
    "upgrade-insecure-requests": "1"
}


class QQ_mail(object):
    def __init__(self):
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_option)
        self.cookies = dict()
        self.sid = ''
        self.mailid_list = []

    def qq_driver_get_cookie(self):
        self.driver.get(
            'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?target=self&appid=522005705&daid=4&s_url=https://mail.qq.com/cgi-bin/readtemplate?check=false%26t=loginpage_new_jump%26vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input_for_xmail440503.css')
        switch_btn = WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'switch_btn')))
        switch_btn.click()

        self.driver.find_element_by_id("u").clear()
        self.driver.find_element_by_id("u").send_keys("284794223")

        self.driver.find_element_by_id("p").clear()
        self.driver.find_element_by_id("p").send_keys("bulibuqi3344..")

        self.driver.find_element_by_id("login_button").click()

        time.sleep(5)
        cookie = self.driver.get_cookies()
        for i in cookie:
            self.cookies[i['name']] = i['value']

        print(self.cookies)

        self.driver.close()

    def received_email(self):
        url = "https://mail.qq.com/cgi-bin/login?vt=passport&vm=wsk&delegate_url="
        login_page2 = requests.get(url=url, headers=headers, verify=False, cookies=self.cookies)
        self.sid = re.search(r'sid=(.*?)&', login_page2.url).group(1)
        print("sid", self.sid)
        self.mail_list(0)

    def mail_list(self, page):
        url_received = "https://mail.qq.com/cgi-bin/mail_list?sid={}&page={}".format(str(self.sid), str(page))
        page_received = requests.get(url=url_received, headers=headers, verify=False, cookies=self.cookies)
        html = etree.HTML(page_received.text)
        # with open('mail_list0', 'r', encoding='gb18030') as f:
        #     page_text = f.read()
        #     html = etree.HTML(page_text)

        div_list = html.xpath("//div[@class = 'toarea']")
        # print(etree.tostring(div_list[0], encoding='utf-8', pretty_print=True, method="html").decode('utf-8'))

        # 获取电子账单的 mailid
        for div in div_list:
            input_list = div.xpath(".//table[@class = 'i M']//td[@class='cx']/input")
            for input in input_list:
                fa = input.xpath('./@fa')
                if fa[0] == 'ccsvc@message.cmbchina.com':
                    td_list = input.xpath("./parent::td")
                    for td in td_list:
                        td_list2 = td.xpath("./following-sibling::*[2]")
                        for td2 in td_list2:
                            td2_text = ''.join(td2.xpath(".//text()"))
                            if "电子账单" in td2_text:
                                onclick = td2.xpath(".//@onclick")[0]
                                self.mailid_list.append(onclick.split(',')[1].replace("'", ''))

        # 获取总页数
        if page == 0:
            all_page = 0
            toolbg_list = html.xpath(".//div[contains(@class,'toolbg')]//text()")
            for toolbg in toolbg_list:
                if "document.write" in toolbg:
                    all_page = int(toolbg.split("(")[1].split("+")[0].replace(" ", ""))
                    break

            for i in range(all_page):
                page = i + 1
                self.mail_list(page)

            self.analy_mail()

    def analy_mail(self):
        for mail in self.mailid_list:
            url = "https://mail.qq.com/cgi-bin/readmail?mailid={}&sid={}".format(str(mail), str(self.sid))
            mail_page = requests.get(url=url, headers=headers, verify=False, cookies=self.cookies)
            html = etree.HTML(mail_page.text)
            # with open('mail11', 'r', encoding='gb18030') as f:
            #     mail_text = f.read()
            #     html = etree.HTML(mail_text)

            font = ''.join(''.join(html.xpath(".//span[@id='fixBand57']//font//text()")).split())
            print(font)

            date = ''.join(''.join(html.xpath(".//span[@id='fixBand18']//font//text()")).split())
            print(date)


if __name__ == '__main__':
    q = QQ_mail()
    q.qq_driver_get_cookie()
    q.received_email()

    # i = "ùo"
