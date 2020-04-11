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
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
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
                    durtime = response.elapsed.microseconds / 1000  # 发起请求和响应到大的时间，单位ms
                    result = {'code': '0000', 'message': '成功', 'data': response.text}
                else:
                    result = {'code': '2004', 'message': '接口返回状态错误', 'data': response.status_code}
            elif interface_url == '':
                result = {'code': '2002', 'message': '接口地址参数为空', 'data': '[]'}
            else:
                result = {'code': '2003', 'message': '接口地址错误', 'data': '[]'}
        except Exception as e:
            result = {'code': '9999', 'message': '系统异常', 'data': e}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        if result['code'] == '0000':
            print("处理HTTP请求成功，返回的数据是：%s" % result['data'])
        elif result['code'] == '9999':
            print("系统异常：%s" % result['data'])
        else:
            print("处理HTTP请求失败：%s，返回的数据是：%s" % (result['message'], result['data']))
        return result

    # GET请求，参数在接口地址后面
    def __http_get(self, interface_url, headerdata, interface_param):
        """
        : param interface_url: 接口地址
        : param headerdata: 请求头文件
        : param interface_param: 接口请求参数
        : return: 字典形式结果
        """
        try:
            if interface_url != '':
                temp_interface_parm = self.__new_param(interface_param)
                if interface_url.endswith('?'):
                    requrl = interface_url+temp_interface_parm
                else:
                    requrl = interface_url+'?'+temp_interface_parm
                response = requests.get(url=requrl, headers=headerdata, verify=False, timeout=10)
                if response.status_code == 200:
                    durtime = response.elapsed.microseconds / 1000  # 发起请求和相应到达的时间，单位ms
                    result = {'code': '0000', 'message': '成功', 'data': response.text}
                else:
                    result = {'code': '3004', 'message': '接口返回状态错误', 'data': response.status_code}
            elif interface_url == '':
                result = {'code': '3002', 'message': '接口地址参数为空', 'data': []}
            else:
                result = {'code': '3003', 'message': '接口地址错误', 'data': []}
        except Exception as e:
            result = {'code': '9999', 'message': '系统异常', 'data': e}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        if result['code'] == '0000':
            print("处理HTTP请求成功，返回的数据是：%s" % result['data'])
        elif result['code'] == '9999':
            print("系统异常：%s" % result['data'])
        else:
            print("处理HTTP请求失败：%s，返回的数据是：%s" % (result['message'], result['data']))
        return result

    # 统一处理HTTP请求
    def http_request(self, interface_url, headerdata, interface_param, request_type):
        """
        : param interface_url: 接口地址
        : param headerdata: 请求头文件
        : param interface_param: 接口请求参数
        : param request_type: 请求类型
        : return: 字典形式结果
        """
        try:
            if request_type == 'get' or request_type == 'GET':
                result = self.__http_get(interface_url, headerdata, interface_param)
            elif request_type == 'post' or request_type == 'POST':
                result = self.__http_post(interface_url, headerdata, interface_param)
            else:
                result = {'code': '1000', 'message': '请求类型错误', 'data': request_type}
        except Exception as e:
            result = {'code': '9999', 'message': '系统异常', 'data': e}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result


if __name__ == "__main__":
    test_interface = RequestInterface()  # 实例化HTTP请求类
    test_db = base_opmysql.OperationDbInterface()  # 实例化SQL处理类
    # result1 = test_interface.http_request('', '', '', 'GET')
    # result2 = test_interface.http_request('http://180.106.83.239:18080/apis/login', '', '{\'employeeno\':\'YG3346\',\'pwd\':\'c33367701511b4f6020ec61ded352059\'}', 'POST')
    sen_sql = "select exe_mode,url_interface,header_interface,params_interface from case_interface where name_interface='getIpInfo.php' and id=1"
    params_interface = test_db.select_one(sen_sql)
    if params_interface['code'] == '0000':
        url_interface = params_interface['data']['url_interface']
        temp = params_interface['data']['header_interface']
        headerdata1 = eval(params_interface['data']['header_interface'])
        param_interface = params_interface['data']['params_interface']
        type_interface = params_interface['data']['exe_mode']
        if url_interface != '' and headerdata1 != '' and param_interface != '' and type_interface != '':
            result1 = test_interface.http_request(interface_url=url_interface, headerdata=headerdata1, interface_param=param_interface, request_type=type_interface)
            if result1['code'] == '0000':
                result_resp = result1['data']
                test_db.op_sql("UPDATE case_interface SET result_interface='%s' WHERE id=1" % result_resp)
                print("处理HTTP请求成功，返回数据是：%s" % result_resp)
            else:
                print("处理HTTP请求失败")
        else:
            print("测试用例中有空值")
    else:
        print("获取接口测试用例数据失败")
