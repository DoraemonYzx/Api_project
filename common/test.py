#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: test.py
@time: 2020/04/24
"""
import requests
import json


def login(s, user="test", paw=123456):
    """
    登录
    :param s: requests.Session()
    :param user: 账号
    :param paw:  密码
    :return: s
    """
    url = "http://49.235.92.12:9000/api/v1/login"
    body = {"username": user,
            "password": paw
            }
    r1 = s.post(url, json=body)
    print(r1.json())
    token = r1.json()["token"]
    h1 = {"Authorization": "Token %s" % token}
    s.headers.update(h1)                                # 将token关联至头部，这样后面的请求就不需要每次都传token
    return s


def update(s, mail):
    """
    修改邮箱
    :param s:
    :param mail:
    :return:
    """
    url3 = "http://49.235.92.12:9000/api/v1/userinfo"
    body1 = {
            "name": "test",
            "sex": "M",
            "age": 20,
            "mail": mail
    }
    r = s.post(url3, json=body1)
    return r.json()


def find(s):
    """
    查询修改后的结果
    :param s:
    :return:
    """
    url1 = "http://49.235.92.12:9000/api/v1/userinfo"
    r = s.get(url1)
    return r.json()


if __name__ == "__main__":
    se = requests.Session()
    login(se, "test", 123456)
    ur = update(se, "123456789@qq.com")
    print(ur)
    fr = find(se)
    print(fr)[图片]
