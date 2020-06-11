import requests, os, execjs
import base64
import random
import re
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}


class QQEmail(object):
    def __init__(self):
        self.sid = ''
        self.new_cookies = dict()
        self.mailid_list = []
        self.cookies = requests.cookies.RequestsCookieJar()
        self.proxy = {'http':'127.0.0.1:1080'}
        # self.proxy = {'http': ''}

    def getPass(self, u, p, verifycode):
        js_path = "%s/qq.js" % "/".join(os.path.abspath(__file__).split("/")[:-1])
        with open(js_path, 'r') as f:
            js_content = f.read()
            ctx = execjs.compile(js_content)
            new_pwd1 = ctx.call("getPassword", u, p, verifycode)
            new_pwd2 = new_pwd1.encode('latin1')
            new_pwd3 = base64.b64encode(new_pwd2)
            new_pwd4 = str(new_pwd3, 'utf-8')
            new_pwd5 = ctx.call("btoaReaplace", new_pwd4)
            return new_pwd5

    def getAction(self):
        js_path = "%s/qq.js" % "/".join(os.path.abspath(__file__).split("/")[:-1])
        with open(js_path, 'r') as f:
            js_content = f.read()
            ctx = execjs.compile(js_content)
            action = ctx.call("getAction")
            return action

    def getParam(self, url):
        resp1 = requests.get(url, headers=headers, verify=False)
        self.cookies.update(resp1.cookies)
        pt_login_sig = self.cookies['pt_login_sig']

        qrsig_url = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=522005705&e=2&l=M&s=3&d=72&v=4&t={}&daid=4&pt_3rd_aid=0".format(
            str(random.random()))
        qrsig_resp = requests.get(qrsig_url, headers=headers, verify=False, cookies=self.cookies)
        self.cookies.update(qrsig_resp.cookies)

        username = 'qq号'
        mima = 'qq密码'

        first_url = "https://ssl.ptlogin2.qq.com/check"

        param_first = {
            'regmaster': '',
            'pt_tea': '2',
            'pt_vcode': '1',
            'uin': username,
            'appid': '522005705',
            'js_ver': '19042519',
            'js_type': '1',
            'login_sig': pt_login_sig,
            'u1': 'https://mail.qq.com/cgi-bin/readtemplate?check=false&t=loginpage_new_jump&vt=passport&vm=wpt&ft=loginpage&target=',
            'r': random.random(),
            'pt_uistyle': '25'

        }

        resp2 = requests.get(first_url, headers=headers, verify=False, params=param_first, cookies=self.cookies)
        self.cookies.update(resp2.cookies)

        pt_vcode_v1 = resp2.text.split("'")[1]
        verifycode = resp2.text.split("'")[3]
        pt_verifysession_v1 = resp2.text.split("'")[7]
        pt_randsalt = resp2.text.split("'")[9]
        ptdrvs = resp2.text.split("'")[11]

        password = self.getPass(username, mima, verifycode)
        action = self.getAction()

        second_url = "https://ssl.ptlogin2.qq.com/login"
        params = {
            'u': username,
            'verifycode': verifycode,
            'pt_vcode_v1': pt_vcode_v1,
            'pt_verifysession_v1': pt_verifysession_v1,
            'p': password,
            'pt_randsalt': pt_randsalt,
            'u1': 'https://mail.qq.com/cgi-bin/readtemplate?check=false&t=loginpage_new_jump&vt=passport&vm=wpt&ft=loginpage&target=&account={}'.format(
                str(username)),
            'ptredirect': '0',
            'h': '1',
            't': '1',
            'g': '1',
            'from_ui': '1',
            'ptlang': '2052',
            'action': action,
            'js_ver': '19042519',
            'js_type': '1',
            'login_sig': pt_login_sig,
            'pt_uistyle': '25',
            'aid': '522005705',
            'daid': '4',
            'ptdrvs': ptdrvs,
        }

        self.cookies['ptui_loginuin'] = username
        resp3 = requests.get(second_url, headers=headers, verify=False, params=params, cookies=self.cookies)

        print(resp3.text)

        self.cookies.update(resp3.cookies)

        ssl_url = resp3.text.split("'")[5]
        # print(ssl_url)
        # 禁止重定向，获取重定向的网址
        ssl_resp = requests.get(ssl_url, headers=headers, verify=False, cookies=self.cookies, allow_redirects=False)
        self.cookies.update(ssl_resp.cookies)
        # 重定向地址
        loc_url = ssl_resp.headers.get('Location')
        loc_resp = requests.get(loc_url, headers=headers, verify=False, cookies=self.cookies)
        self.cookies.update(loc_resp.cookies)
        ptn1 = re.compile(r'top\.location\.href = "(.*?)"')
        sid_url = re.search(ptn1, loc_resp.text).group(1)
        sid_resp = requests.get(sid_url, headers=headers, verify=False, cookies=self.cookies, allow_redirects=False)
        self.cookies.update(sid_resp.cookies)
        frame_url = sid_resp.headers.get('Location')
        ptn2 = re.compile(r'sid=(.*?)&r')
        self.sid = re.search(ptn2, frame_url).group(1)

        frame_resp = requests.get(frame_url, headers=headers, verify=False, cookies=self.cookies)
        # self.cookies.update(frame_resp.cookies.get_dict())

        self.cookies.update(frame_resp.cookies)

        print(self.cookies)

    def getMailList(self, page):
        url_received = "https://mail.qq.com/cgi-bin/mail_list?sid={}&page={}".format(str(self.sid), str(page))
        page_received = requests.get(url=url_received, headers=headers, verify=False, cookies=self.cookies, proxies=self.proxy)
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
                self.getMailList(page)

            self.getMailOne()

    def getMailOne(self):
        for mail in self.mailid_list:
            url = "https://mail.qq.com/cgi-bin/readmail?mailid={}&sid={}".format(str(mail), str(self.sid))
            mail_page = requests.get(url=url, headers=headers, verify=False, cookies=self.cookies, proxies=self.proxy)
            html = etree.HTML(mail_page.text)
            font = ''.join(''.join(html.xpath(".//span[@id='fixBand57']//font//text()")).split())
            print(font)

            date = ''.join(''.join(html.xpath(".//span[@id='fixBand18']//font//text()")).split())
            print(date)

    def getProxy(self):
        a = requests.get("http://httpbin.org/get", proxies=self.proxy)
        print(a.text)


if __name__ == '__main__':
    url = "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?target=self&appid=522005705&daid=4&" \
          "s_url=https://mail.qq.com/cgi-bin/readtemplate?" \
          "check=false%26t=loginpage_new_jump%26vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&" \
          "low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&" \
          "self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&" \
          "pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&" \
          "css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input_for_xmail440503.css"
    q = QQEmail()
    q.getParam(url)
    # q.getMailList(0)
    # q.getProxy()
