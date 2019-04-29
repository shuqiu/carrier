import base64

import requests
from Crypto.PublicKey import RSA
from lxml import etree
from numpy import long
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# def login():
#     userid = 15879087387
#     password = 120041
#
#     # 记录cookie
#     cookies = dict()
#
#     # 首次登陆
#     first_url = "https://jx.ac.10086.cn/login"
#     headers1 = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "Referer": "http://www.jx.10086.cn/__index.html"
#     }
#
#     resp = requests.get(first_url, headers=headers1, verify=False)
#
#     # selector = etree.HTML(resp.text)
#     # login_sid = selector.xpath('//*[@id="normal-user"]/input[3]/@value')[0]
#     # login_spid = selector.xpath('//*[@id="normal-user"]/input[7]/@value')[0]
#
#     cookies.update(resp.cookies.get_dict())
#
#     # 2
#     second_url = "https://login.10086.cn/SSOCheck.action?channelID=40791&backUrl=https://211.141.90.208/SSOArtifact?spid=C3CB56021D65C9D00C442C3F2005762179D3EB74C5F30D6A55F45727D83842E3DD901D9B7459D8E2&RelayState=type=A;backurl=http://www.jx.10086.cn/my/;nl=3;loginFrom=null;refer=null"
#
#     headers2 = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
#         # "Host": "login.10086.cn",
#         "Referer": "https://jx.ac.10086.cn/login",
#         # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
#     }
#
#     resp2 = requests.get(second_url, headers=headers2, verify=False)
#
#
#     # 3 获取图像验证码
#     image_url = 'https://jx.ac.10086.cn/common/image.jsp'
#     headers3 = {
#         "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
#         "Referer": "https://jx.ac.10086.cn/login"
#     }
#     resp3 = requests.get(image_url, headers=headers3, verify=False, cookies=cookies)
#     with open('captcha.jpg', 'wb') as f:
#         f.write(resp.content)
#     captcha_code = input('please input captcha....')
#     cookies.update(resp3.cookies.get_dict())
#
#     print(cookies)
#
#     # 4
#     # four_url = "https://jx.ac.10086.cn/Login"
#     # login_data = {
#     #     'validCode':captcha_code
#     # }
#     #
#     # resp4 = requests.post(four_url, headers=headers3, data=login_data,verify=False, cookies=cookies)
#     # print(resp4.status_code)
#
#     # login_url = "https://jx.ac.10086.cn/Login"
#     # login_data = {
#     #     "from": "yanhuang",
#     #     "sid": login_sid,
#     #     "type": 'B',
#     #     "backurl": "https://jx.ac.10086.cn/4login/backPage.jsp",
#     #     "errorurl": "https://jx.ac.10086.cn/4login/errorPage.jsp",
#     #     "spid": login_spid,
#     #     "RelayState": "type=A;backurl=http://www.jx.10086.cn/my/;nl=3;loginFrom=null;refer=null",
#     #     "mobileNum": userid,
#     #     "servicePassword": password,
#     #     "smsValidCode": "",
#     #     "validCode": captcha_code,
#     # }
#     #
#     # headers = {
#     #     "Content-Type": "application/x-www-form-urlencoded",
#     #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     #     "Referer": "https://jx.ac.10086.cn/login"
#     # }
#     # resp4 = requests.post(login_url, data=login_data, headers=headers)
#     # print(resp4.text)
#     # print(resp4.cookies)
#
#
# def get_encrypt_serPwd(serPwd):
#     headers = {
#         'X-Requested-With': 'XMLHttpRequest',
#     }
#     url = 'http://gd.ac.10086.cn/ucs/ucs/decryptToken/generate.jsps'
#     resp = requests.get(url, headers=headers,verify=False)
#     random_key = resp.json()['decryptToken']
#     # 公钥
#     public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuX8iFyL8TZGlhxG0imA+L2CslQZ0wqI5JyfC9OO9BdHlymySpnF1mTOKGQFexx825LtKPVsar2unCTMhW7aCHF/uqTpRdae+23nCMvAjUOyDTDk8Eut1j1or+36C0BLVEQCsTPe29qAPUM0Qr3CzFoU0LCXSqTVsCvjR9S04KcZGQzcWZ9hxv/fYVHgcC/OoHEvF+Xj4nPaqIRqC1+WjyHFZ3WQmCNXTI1xoo6/jnw5zRvJ08/8nR7UhbPweDwecHoZjUImC2C8MLfsTuxWH9QYacuzodk8oMrhb023B7jamVknNRw+lH3WaOZshSgR4lTYMcv3dvWvI+9jyGK6T7wIDAQAB"
#     publik_key = """-----BEGIN PUBLIC KEY-----
#     {}
#     -----END PUBLIC KEY-----""".format(public_key)
#
#     # plain_text = 'serPwd:' + serPwd + '|randomKey:' + random_key
#     rsakey = RSA.importKey(publik_key)
#
#     print(rsakey)
    # cipher = Cipher_pkcs1_v1_5.new(rsakey)
    # cipher_text = base64.b64encode(cipher.encrypt(plain_text.encode('utf-8')))
    #
    # return cipher_text