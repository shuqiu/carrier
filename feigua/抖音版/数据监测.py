import requests

headers = {
    "Host": "dy.feigua.cn",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Referer": "https://dy.feigua.cn/Member",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

cookies = {
    # "Hm_lvt_b9de64757508c82eff06065c30f71250": "1578466213",
    # "chl": "key=feigua2",
    # "Hm_lpvt_b9de64757508c82eff06065c30f71250": "1578466225",
    # "_uab_collina": "157846622517020118898476",
    # "ASP.NET_SessionId": "w5nv1jch0majfdmys2pbkvsd",
    # "FEIGUA": "UserId=d8e9d6b1da00c091ecda4f7bbae2c650&NickName=20f3035a43719b9b&checksum=64d4f0d6d205&FEIGUALIMITID=12dbf5f497c64e3690b934b219f721c0",
    "FEIGUAUNIONID": "094ba700f9fcf3715ee415232243cb0fa2eac274a5a9d7f458431a779188cbcf",
}


def my_dy():
    """
    我的抖音号
    """

    key = "197472929"
    url = "https://dy.feigua.cn/Focus/SearchByShortId"
    params = {
        "keyword": key
    }

    resp = requests.post(url=url, data=params, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def my_authorize():
    """
    我的授权
    """
    key = "197472929"
    url = "https://dy.feigua.cn/MyAuthorize/SearchByShortId"
    params = {
        "keyword": key
    }

    resp = requests.post(url=url, data=params, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def video_monitor():
    """
    视频监控
    """

    url = "https://dy.feigua.cn/Track/SearchAwemeByUrl"
    key = "https://www.douyin.com/share/video/6779358707617713422/?mid=6779223167459150599"

    params = {
        "keyword": key
    }

    # resp = requests.post(url=url, data=params, headers=headers, cookies=cookies, verify=False)
    # print(resp.text)

    """
    开始监控
    """

    url = "https://dy.feigua.cn/Track/AddImmediateTrack"
    params = {
        "awemeId":"6779358707617713422",
        "bloggerUid": "102217477530",
        "title": "#历史上的今天 周恩来总理逝世朱德叶剑英邓小平等吊唁#缅怀总理周恩来 #致敬 #107头条 #家国档案70年",
        "awemeUrl": "https://www.douyin.com/share/video/6779358707617713422/?mid=6779223167459150599",
        "logoUrl": "https://p9-dy.byteimg.com/img/tos-cn-p-0015/c79ea3569e2a4e85afb6d88c6fe9665f_1578442482~c5_300x400.jpeg?from=2563711402_large",
        "pubTime": "2020/1/8 8:14:34",
        "bloggerNickName": "浙江城市之声",
        "hourType": "1",
        "bloggerAvatar":"https://p3-dy.byteimg.com/aweme/720x720/241060006856aa43e06d6.jpeg",
        "isRemind": "0",
        "maxLikeNumber": "",
        "likeNumber": "6404866",
        "promotionId": ""
    }

    # resp = requests.post(url=url, data=params, headers=headers, cookies=cookies, verify=False)
    # print(resp.text)

    """
    监控历史
    """

    url = "https://dy.feigua.cn/Track/History"
    resp = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


if __name__ == '__main__':
    # hot_video()
    video_monitor()
