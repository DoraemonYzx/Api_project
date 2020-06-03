#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: test_case.py
@time: 2020/04/22
"""
from public import config
import json
import unittest
from common.base_request import RequestInterface
from common.base_compare import CompareParm
from public import config
import json
import ddt
from data import interface_select_data

r = RequestInterface()
compare = CompareParm()


class TestCase(object):
    def __init__(self):
        self.response = ""

    def test_case_assert(self, result, compare_code, compare_params):
        # if result['code'] == '0000' and compare_code['code'] == '0000' and compare_params['code'] == '0000' and result['durtime'] < 1.5:
        #     return True
        # else:
        #     return False
        if result['code'] != '0000':
            print("XXXXXXXXXXXXXXXX\n返回状态码不是200\nXXXXXXXXXXXXXXXX")
            return False
        else:
            if compare_code['code'] != '0000':
                print("XXXXXXXXXXXXXXXX\n定义的关键值和预期结果不符\nXXXXXXXXXXXXXXXX")
                return False
            else:
                if compare_params['code'] != '0000':
                    print("XXXXXXXXXXXXXXXX\n返回的参数完整性校验失败\nXXXXXXXXXXXXXXXX")
                    return False
                else:
                    if result['durtime'] > 1.5:
                        print("XXXXXXXXXXXXXXXX\n请求响应时间大于1.5秒需要优化\nXXXXXXXXXXXXXXXX")
                        return False
                    else:
                        print("测试通过\n****************")
                        return True

    def test_case(self, datalist):
        print("\n****************\n接口描述：%s\n请求入参是:%s" % (datalist['interface'], datalist['msg']))
        url = config.base_url + datalist['url']
        result = r.http_request(interface_url=url, headerdata=datalist['h'],
                                interface_param=datalist['d'], request_type=datalist['mode'])
        compare_code = compare.compare_code(result_interface=result['data'], code=datalist['code'],
                                            expected_code=datalist['expected_code'])
        compare_params = compare.compare_params_complete(result_interface=result['data'],
                                                         params_to_compare=json.dumps(datalist['expected_key']))
        bool_result = self.test_case_assert(result, compare_code, compare_params)
        self.response = result
        return bool_result
