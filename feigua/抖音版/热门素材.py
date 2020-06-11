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


def hot_video():
    """
    热门视频
    普通会员只能查看50个
    """

    url = "https://dy.feigua.cn/Aweme/Search"

    params = {
        "keyword": "",
        "tag": "",
        "likes": "0",
        "hours": "24",  # 近3天：72  近7天：168  近15天：360  近30天：720
        "duration": "0",
        "gender": "0",
        "age": "0",
        "province": "0",
        "city": "0",
        "sort": "3",  # 综合排序：0  点赞最多：1  评论最多：2  分享最多：3
        "ispromotions": "0",
        "page": "1"
    }

    resp = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def video_detail():
    """
    视频详情
    """
    url = "https://dy.feigua.cn/Aweme/Detail"

    params = {
        "id": "7058270",
        "awemeId": "6779358707617713422",
        "active": "detail",
        "logtype": "0"
    }

    # resp = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=False)
    # print(resp.text)

    """
    视频详情
    """

    url = "https://dy.feigua.cn/Aweme/GetAwemeDetail"
    params = {
        "id": "7058270",
        "awemeId": "6779358707617713422",
        "promotionId": ""
    }

    resp = requests.post(url=url, params=params, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def hot_music():
    """
    热门音乐
    普通会员只能查看10个
    """

    url = "https://dy.feigua.cn/Music"

    params = {
        "keyword": "",
        "hours": "24",
        "sort": "0",
        "page": "1"
    }

    resp = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def hot_topic():
    """
    热门话题
    普通会员只能查看10个
    """

    url = "https://dy.feigua.cn/Topic"

    params = {
        "keyword": "",
        "hours": "24",
        "sort": "0",
        "page": "1"
    }

    resp = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def hot_comment():
    """
    热门评论
    普通会员只能查看5个
    """

    url = "https://dy.feigua.cn/Comment"

    resp = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def hot_aweme_today():
    """
    今日热门视频
    普通会员只能查看5个
    """
    url = "https://dy.feigua.cn/HotAweme/Minute"
    url = "https://dy.feigua.cn/HotAweme/Daily"
    resp = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def favorite():
    """
    我收藏的素材
    """

    # 播主收藏 0   视频收藏 1   音乐收藏 2   话题收藏 3  商品收藏 4
    url = "https://dy.feigua.cn/Favorite?type=4"
    resp = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


if __name__ == '__main__':
    # hot_video()
    video_detail()
