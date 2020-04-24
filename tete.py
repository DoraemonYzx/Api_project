#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: tete.py
@time: 2020/04/21
"""
import requests
interface_url = "https://testapicxcm.cxjk.com/interface/home/growChangeByDay"
headerdata = {
"Content-Type":"application/x-www-form-urlencoded"
}
d = {
    "week": "21"
}

response = requests.post(url=interface_url, headers=headerdata,data=d, verify=False, timeout=10)
print(response.status_code)
print(response.text)