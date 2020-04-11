#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: compare.py
@time: 2020/04/09
"""
import json
import logging
import os
from common import base_opmysql
from common import base_request
from public import config
"""
定义数据比较方法
1.compare_param是对外的参数比较类
2.compare_code是关键参数值的比较方法，compare_params_complete是参数完整性的比较方法
3.get_compare_params是获得返回包数据去重后集合的方法
4.recur_params递归操作方法，辅助去重
"""
operation_db = base_opmysql.OperationDbInterface()  # 实例化测试数据库操作类


class CompareParm(object):
    # 初始化数据
    def __init__(self, params_interface):
        self.params_interface = params_interface  # 接口入参
        self.id_case = params_interface['id']  # 测试用ID
        self.result_list_response = []  # 定义用来存储参数集的空列表
        self.params_to_compare = params_interface['params_to_compare']  # 定义参数完整性的预期结果

    # 定义关键参数值(code)比较
    def compare_code(self, result_interface):
        """
        :param result_interface: HTTP返回包数据
        :return: 返回信息message，数据data
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)  # 将字符类型转换成字典类型
                print("temp_result_interface= %s" % temp_result_interface)
                temp_code_to_compare = self.params_interface['code_to_compare']  # 获取待比较code的名称
                print("temp_code_to_compare = %s" % temp_code_to_compare)
                if temp_code_to_compare in temp_result_interface.keys():
                    if str(temp_result_interface[temp_code_to_compare]) == str(self.params_interface['code_expect']):
                        result = {'code': '0000', 'message': '关键字参数值相同', 'data': []}
                        operation_db.op_sql("UPDATE case_interface set code_actual='%s',result_code_compare=%s where id=%s" %
                                            (temp_result_interface[temp_code_to_compare], 1, self.id_case))
                    elif str(temp_result_interface[temp_code_to_compare]) != str(self.params_interface['code_expect']):
                        result = {'code': '1003', 'message': '关键字参数值不相同', 'data': []}
                        operation_db.op_sql("UPDATE case_interface set code_actual='%s',result_code_compare=%s where id=%s" %
                                            (temp_result_interface[temp_code_to_compare], 0, self.id_case))
                    else:
                        result = {'code': '1002', 'message': '关键字参数值比较出错', 'data': []}
                        operation_db.op_sql("UPDATE case_interface set code_actual='%s',result_code_compare=%s where id=%s" %
                                            (temp_result_interface[temp_code_to_compare], 3, self.id_case))
                else:
                    result = {'code': '1001', 'message': '返回包数据无关键值参数', 'data': []}
                    operation_db.op_sql("UPDATE case_interface set result_code_compare=%s where id=%s" %
                                        (2, self.id_case))
            else:
                result = {'code': '1000', 'message': '返回包格式不合法', 'data': []}
                operation_db.op_sql("UPDATE case_interface set result_code_compare=%s where id=%s" % (4, self.id_case))
        except Exception as e:
            result = {'code': '9999', 'message': '关键值参数比较异常', 'data': e}
            operation_db.op_sql("UPDATE case_interface set result_code_compare=%s where id=%s" % (9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
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
            operation_db.op_sql("UPDATE case_interface set result_code_compare=%s where id=%s" % (9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 参数完整性比较方法，比较传参值与__recur_params方法返回的结果
    def compare_params_complete(self, result_interface):
        """
        :param result_interface: 接口http返回包
        :result: 返回码code,返回信息message,返回数据data
        """
        try:
            temp_compare_params = self.__recur_params(result_interface)  # 获取返回包参数合集
            if temp_compare_params['code'] == '0000':
                temp_result_list_response = temp_compare_params['data']  # 获取接口返回参数去重列表
                if self.params_to_compare.startswith('[') and isinstance(self.params_to_compare, str):  # 判断用例中预期结果是否为列表
                    list_params_to_compare = eval(self.params_to_compare)  # 将数据库表unicode编码数据转换成原列表
                    if set(list_params_to_compare).issubset(set(temp_result_list_response)):  # 集合的包含关系
                        result = {'code': '0000', 'message': '参数完整性比较一致', 'data': []}
                        operation_db.op_sql('UPDATE case_interface set params_actual="%s",result_params_compare=%s where id="%s"' %
                                            (temp_result_list_response, 1, self.id_case))
                    else:
                        result = {'code': '3001', 'message': '实际结果中元素不都在预期结果中', 'data': []}
                        operation_db.op_sql('UPDATE case_interface set params_actual="%s",result_params_compare=%s where id="%s"' %
                                            (temp_result_list_response, 0, self.id_case))
                else:
                    result = {'code': '4001', 'message': '用例中待比较参数集错误', 'data': self.params_to_compare}
            else:
                result = {'code': '2001', 'message': '调用__recur_params方法返回错误', 'data': []}
                operation_db.op_sql('UPDATE case_interface set result_params_compare=%s where id="%s"' %
                                    (2, self.id_case))
        except Exception as e:
            result = {'code': '9999', 'message': '参数完整性比较异常', 'data': e}
            operation_db.op_sql("UPDATE case_interface set result_code_compare=%s where id=%s" % (9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 定义递归操作,将接口返回数据中的参数名写入列表中(去重)
    def __recur_params(self, result_interface):
        try:
            print("调用__recur_paramsf方法")
            print(result_interface)
            if isinstance(result_interface, str):  # 入参是字符串类型且能被转换成字典
                temp_result_interface = json.loads(result_interface)
                print(temp_result_interface)
                self.__recur_params(temp_result_interface)
            elif isinstance(result_interface, dict):  # 入参是字典
                print("进入elif")
                for key, value in result_interface.items():
                    self.result_list_response.append(key)
                    if isinstance(value, list):
                        for key in value:
                            self.__recur_params(key)
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


if __name__ == "__main__":
    sen_sql = "select * from case_interface where name_interface='getIpInfo.php' and id =1"
    params_interface1 = operation_db.select_one(sen_sql)
    result_interface1 = params_interface1['data']['result_interface']
    test_compare_param = CompareParm(params_interface1['data'])
    result_compare_code = test_compare_param.compare_code(result_interface1)  # 关键值参数比较
    print(result_compare_code)
    result_compare_params_complete = test_compare_param.compare_params_complete(result_interface1)  # 参数完整性比较
    print(result_compare_params_complete)
