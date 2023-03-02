#!python3
# -*- coding:utf8 -*-

# pip3 install requests

import requests

proxies = {
    "http": "http://127.0.0.1:3517",
    "https": "http://127.0.0.1:3517",
}

# r = requests.get("https://www.baidu.com/", proxies=proxies)
# r = requests.get("https://www.bing.com/", proxies=proxies)
r = requests.get("https://wiki.yijunjun.site/")

print(r.headers)
# print(r.text)
