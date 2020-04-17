#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: session.py
@time: 2020/04/13
"""
import requests
from selenium import webdriver

"""
案例一：通过抓包获取cookies,往session中增加cookies绕过登录验证码,但是写死cookies不利于自动化测试
"""
# 定义session
s = requests.session()
# 定义接口地址
url = '接口地址'
#  更新之前的cookies
print(s.cookies)
# 实例化一个CookieJar包c
c = requests.cookies.RequestsCookieJar()
# 在CookieJar包c中添加cookie
c.set("cookicName1", "cookieValue1")
c.set("cookicName2", "cookieValue2")
# 在session中更新cookies
s.cookies.update(c)
# 更新之后的cookies
print(s.cookies)
# 通过session发GET请求
r1 = s.get(url, verify=False)
print(r1.text)

"""
案例二：使用selenium加载浏览器缓存,进入页面,使用本地浏览器缓存自动登录后获取cookies增加到session中（推荐）
       前提：需要手工登录一次后,保持登录状态,重新进入页面是已经登录状态
       或者：测试环境让开发去掉验证码或者写死一个值,通过seleium完成登录后获取cookies增加到session中（推荐）
"""
# 浏览器缓存文件夹路径
profile_directory = r'浏览器缓存文件夹路径'

# Chrome浏览器加载缓存文件
profile = webdriver.ChromeOptions()
profile.add_argument(profile_directory)
driver = webdriver.Chrome(profile)
# 打开网页
driver.get("url")
# 获取cookies  格式是字典格式的
cookies = driver.get_cookies()

# FireFox浏览器加载缓存文件
profile = webdriver.FirefoxProfile(profile_directory)
driver1 = webdriver.Firefox(profile)
# 打开网页
driver1.get("url")
# 获取cookies  格式是字典格式的
cookies1 = driver.get_cookies()

# 在session中更新获取到的cookies
s1 = requests.session()
# 实例化一个CookieJar包c1
c1 = requests.cookies.RequestsCookieJar()
# 通过循环,将获取到的cookies写入到c1中
for i in cookies:
    c1.set(i["name"], i["value"])
# 在session中更新cookies
s.cookies.update(c1)

"""
案例三：接口中有动态的cookies或者token等参数值防止代码重复请求
       思路：
       1、找到cookies或者token等动态参数是从哪个接口返回的
       2、请求该接口通过正则或者BeautifulSoup框架(用来获取html格式中的数据)来获取cookies或者token值
       3、传给下一个需要用到的接口
       header={"cookies":getcookies['cooiues']
               "token":gettoken['token']
              }
"""
"""
案例四：接口会检测是否用代码请求
       解决办法：
       1、手工请求接口,复制下User_Agent值
       2、代码请求接口时,在header中增加User_Agent,伪造浏览器请求
"""
