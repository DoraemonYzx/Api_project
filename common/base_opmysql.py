#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: base_opmysql.py
@time: 2020/04/03
"""

import os
import pymysql
import logging
from public import config
"""
定义对MySql数据库的基本操作的封装
1.包含基本的单条语句操作，如删除，修改，更新
2.独立的查询单条，多条数据
3.独立的添加多条数据
"""


class OperationDbInterface:

    def __init__(self,
                 host_db='180.106.83.239',
                 user_db='root',
                 passwd_db="Cloud@18915898007",
                 name_db='cxjk_xspt',
                 port_db=46986,
                 link_type=0):
        print("初始化数据库连接")
        """
        定义初始化数据库连接
        :param host_db: 数据库服务主机
        :param user_db: 数据库用户名
        :param passwd_db: 数据库密码
        :param name_db: 数据库名称
        :param port_db: 端口号，整形数据
        :param link_type: 链接类型，用于设置输出数据是元祖还是字典，默认是字典，link_type=0
        """
        try:
            if link_type == 0:
                # 创建数据库连接,返回字典格式
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            else:
                # 创建数据库连接,返回元祖格式
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8')
            self.cur = self.conn.cursor()
            print("数据库连接成功|数据库为：%s" % name_db)

        except pymysql.Error as e:
            print("创建数据库连接失败|Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path+'/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)

    # 定义单条数据操作，包含删除、更新操作
    def op_sql(self, condition):
        """
        定义单条数据操作，包含删除、更新操作
        :param condition: SQL语句，该通用方法可以用来替代updataone,deleteone
        :return: 字典形式
        """
        try:
            self.cur.execute(condition)  # 执行SQL语句
            self.conn.commit()  # 提交游标数据
            result = {'code': '0000', 'message': '执行通用操作成功', 'data': []}

        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'message': '执行通用操作异常', 'data': []}
            print("数据库错误|op_sql %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        if result['code'] == '0000':
            print("数据为:%s" % result['data'], result['message'])
        else:
            print(result['message'])
        return result

    # 查询表中的单条数据
    def select_one(self, condition):
        """
        查询表中的单条数据
        :param condition: SQL数据
        :return: 字典形式的单条查询结果
        """
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:  # 查询结果返回数据大于0
                results = self.cur.fetchone()  # 获取一条结果
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': []}
        except pymysql.Error as e:
            self. conn.rollback()
            result = {'code': '9999', 'message': '执行单条查询异常', 'data': []}
            print("数据库错误|select_one %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        if result['code'] == '0000':
            print("数据为:%s" % result['data'], result['message'])
        else:
            print(result['message'])
        return result

    # 查询表中多条数据
    def select_all(self, condition):
        """
        查询表中多条数据
        :param condition: SQL语句
        :return: 字典形式的批量查询结果
        """
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:  # 查询结果返回数据大于0
                self.cur.scroll(0, mode='absolute')  # 将鼠标光标放回到初始位置
                results = self.cur.fetchall()  # 返回游标中的所有数据
                result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行批量查询操作异常', 'data': []}
            print("数据库错误|select_all %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        if result['code'] == '0000':
            print("数据为:%s" % result['data'], result['message'])
        else:
            print(result['message'])
        return result

    # 表中插入数据操作
    def insert_data(self, condition, params):
        """
        表中插入数据操作
        :param condition: insert语句
        :param params: insert数据，列表形式[('3','Tom','1 year 1 class','6'),('3','Jack','2 year 1 class','7'),]
        :return: 字典形式的批量插入数据结果
        """
        try:
            results = self.cur.executemany(condition, params)  # 返回插入的数据条数
            self.conn.commit()
            result = {'code': '0000', 'message': '执行插入数据操作成功', 'data': results}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行插入数据操作异常', 'data': []}
            print("数据库错误|insert_data %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        if result['code'] == '0000':
            print("插入的数据条数:%s" % result['data'], result['message'])
        else:
            print(result['message'])
        return result

    # def __del__(self):
    #     if self.cur is not None:
    #         self.cur.close()  # 关闭游标
    #     if self.conn is not None:
    #         self.conn.close()  # 释放数据库资源


if __name__ == "__main__":
    test = OperationDbInterface()  # 实例化类
    result_select_all = test.select_all("SELECT * FROM xk_rate")  # 查询多条数据

    result_select_one = test.select_one("select * from xk_rate where id=16")  # 查询单条数据

    result_op_sql = test.op_sql("update xk_rate set departmentname='上海学术组1' where id=16")

    # 数据库插入操作
    result_insert_data = test.insert_data("insert into xk_rate(id,departmentno,departmentname,tatalpatient,xkpatient)"
                                          "values(%s,%s,%s,%s,%s)", [('31', 'JDEP50000081', '上海学术组', '14732', '1281'),
                                                                     ('32', 'JDEP50000081', '上海学术组', '14732', '1281')])
