#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: base_request.py
@time: 2020/04/07
"""

import requests
import os
import logging
from common import base_opmysql
from public import config

"""
封装HTTP请求操作
1.http_request是主方法，直接供外部调用
2.__hppt_get、__http_post是实际底层分类调用的方法
"""


class RequestInterface(object):

    # 定义处理不同类型的请求参数，包含字典、字符串、空值
    def __new_param(self, param):
        try:
            # 如果接口请求参数是一个字符串类型的字典
            if isinstance(param, str) and param.startswith('{'):
                new_param = eval(param)
            elif param is None:
                new_param = ''
            else:
                new_param = param
        except Exception as e:  # 记录日志到log.txt文件
            new_param = ""
            logging.basicConfig(filename=config.src_path + 'log/syserror.log', level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return new_param

    # POST请求，参数在body中
    def __http_post(self, interface_url, headerdata, interface_param):
        """
        :param interface_url: 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :return: 字典形式结果
        """
        try:
            if interface_url != '':
                temp_interface_param = self.__new_param(interface_param)
                response = requests.post(url=interface_url, headers=headerdata, data=temp_interface_param, verify=False, timeout=10)
                if response.status_code == 200:
                    durtime = response.elapsed.microseconds / 1000  # 发起请求和相应到大的时间，单位ms
                    result = {'code': '0000', 'message': '成功', 'data': response.text}
                else:
                    result = {'code': '2004', 'message': '接口返回状态错误', 'data': '[]'}
            elif interface_url == '':
                result = {'code': '2002', 'message': '接口地址参数为空', 'data': '[]'}
            else:
                result = {'code': '2003', 'message': '接口地址错误', 'data': '[]'}
        except Exception as e:
            result = {'code': '9999', 'message': '系统异常', 'data': '[]'}
            logging.basicConfig(filename=config.src_path + 'log/syserror.log', level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # GET请求，参数在接口地址后面
    def __http_get(self, interface_url, headerdata, interface_param):
        pass

    # 统一处理HTTP请求
    def http_request(self, interface_url, headerdata, interface_param, request_type):
        pass


if __name__ == "__main__":
    test_interface = RequestInterface()  # 实例化HTTP请求类
    test_db = base_opmysql.OperationDbInterface()  # 实例化SQL处理类
