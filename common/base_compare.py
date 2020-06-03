#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: compare.py
@time: 2020/04/09
"""
import json
import logging
from public import config
"""
定义数据比较方法
1.compare_param是对外的参数比较类
2.compare_code是关键参数值的比较方法，compare_params_complete是参数完整性的比较方法
3.get_compare_params是获得返回包数据去重后集合的方法
4.recur_params递归操作方法，辅助去重
"""


class CompareParm(object):
    # 初始化数据
    def __init__(self):
        self.result_list_response = []  # 定义用来存储参数集的空列表
        # # self.result_list_response.clear()
        # print(self.result_list_response)

    # 定义关键参数值(code)比较
    @staticmethod
    def compare_code(result_interface, code, expected_code):
        """
        :param result_interface: HTTP返回包数据
        :param code: 需要比对的code名
        :param expected_code: 预期code值
        :return: 返回信息message，数据data
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)  # 将字符类型转换成字典类型
                temp_code_to_compare = code  # 获取待比较code的名称
                if temp_code_to_compare in temp_result_interface.keys():
                    if str(temp_result_interface[temp_code_to_compare]) == str(expected_code):
                        result = {'code': '0000', 'message': '关键字参数值相同', 'param': code, 'expected_code': str(expected_code),
                                  'actual_key': str(temp_result_interface[temp_code_to_compare])}
                    elif str(temp_result_interface[temp_code_to_compare]) != str(expected_code):
                        result = {'code': '1003', 'message': '关键字参数值不相同', 'param': code, 'expected_code': str(expected_code),
                                  'actual_key': str(temp_result_interface[temp_code_to_compare])}
                    else:
                        result = {'code': '1002', 'message': '关键字参数值比较出错', 'param': code, 'expected_code': str(expected_code),
                                  'actual_key': str(temp_result_interface[temp_code_to_compare])}
                else:
                    result = {'code': '1001', 'message': '返回包数据无关键值参数', 'param': code, 'expected_code': str(expected_code),
                              'actual_key': str(temp_result_interface[temp_code_to_compare])}
            else:
                result = {'code': '1000', 'message': '返回包格式不合法', 'param': code, 'expected_code': str(expected_code), 'actual_key': ''}
        except Exception as e:
            result = {'code': '9999', 'message': '关键值参数比较异常', 'data': e}
            print(result['message'])
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        print("message：%s\n待比较参数名称为：%s\n预期参数值为：%s\n实际参数值为：%s\n****************" %
              (result['message'], result['param'], result['expected_code'], result['actual_key']))
        return result

    # 定义将接口返回数据中的参数名写入列表中
    def get_compare_params(self, result_interface):
        """
        :param result_interface: HTTP返回包数据
        :return: 返回码code,返回信息message,数据data
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)
                self.result_list_response = temp_result_interface.keys()
                result = {'code': '0000', 'message': '成功', 'data': self.result_list_response}
            else:
                result = {'code': '1000', 'message': '返回包格式不合法', 'data': []}
        except Exception as e:
            result = {'code': '9999', 'message': '处理数据异常', 'data': e}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 参数完整性比较方法，比较传参值与__recur_params方法返回的结果
    def compare_params_complete(self, result_interface, params_to_compare):
        """
        :param params_to_compare:
        :param result_interface: 接口http返回包
        :result: 返回码code,返回信息message,返回数据data
        """
        self.result_list_response.clear()
        try:
            temp_compare_params = self.__recur_params(result_interface)  # 获取返回包参数合集
            if temp_compare_params['code'] == '0000':
                temp_result_list_response = temp_compare_params['data']  # 获取接口返回参数去重列表
                if isinstance(params_to_compare, str):  # 判断用例中预期结果是否为列表
                    list_params_to_compare = eval(params_to_compare)  # 将数据库表unicode编码数据转换成原列表
                    if set(list_params_to_compare).issubset(set(temp_result_list_response)):  # 集合的包含关系
                        result = {'code': '0000', 'message': '参数完整性比较一致', 'expected_key': set(list_params_to_compare),
                                  'actual_key': set(temp_result_list_response), 'expected_type': type(params_to_compare)}
                    else:
                        result = {'code': '3001', 'message': '实际结果中元素不都在预期结果中', 'expected_key': set(list_params_to_compare),
                                  'actual_key': set(temp_result_list_response), 'expected_type': type(params_to_compare)}

                else:
                    result = {'code': '4001', 'message': '用例中待比较参数集错误不是str', 'expected_key': '',
                              'actual_key': set(temp_result_list_response), 'expected_type': type(params_to_compare)}
            else:
                result = {'code': '2001', 'message': '调用__recur_params方法返回错误', 'expected_key': '',
                          'actual_key': '', 'expected_type': type(params_to_compare)}
        except Exception as e:
            result = {'code': '9999', 'message': '参数完整性比较异常', 'expected_key': '', 'actual_key': '',
                      'expected_type': type(params_to_compare)}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        print("message：%s\n'预期返回参数为：%s\n实际返回参数为：%s\n预期返回参数集合类型为：%s\n****************" %
              (result['message'], result['expected_key'], result['actual_key'], result['expected_type']))
        for i in result['expected_key']:
            if i not in result['actual_key']:
                print("没有返回的必须参数为:%s" % i)
        return result

    # 定义递归操作,将接口返回数据中的参数名写入列表中(去重)
    def __recur_params(self, result_interface):
        try:
            if isinstance(result_interface, str):  # 入参是字符串类型且能被转换成字典
                temp_result_interface = json.loads(result_interface)
                self.__recur_params(temp_result_interface)
            elif isinstance(result_interface, dict):  # 入参是字典
                for key, value in result_interface.items():
                    self.result_list_response.append(key)
                    if isinstance(value, list):
                        for key1 in value:
                            self.__recur_params(key1)
                    elif isinstance(value, dict):
                        self.__recur_params(value)
                    else:
                        continue
            else:
                pass
        except Exception as e:
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return {'code': '9999', 'message': '处理数据异常', 'data': e}
        return {'code': '0000', 'message': '成功', 'data': list(set(self.result_list_response))}
