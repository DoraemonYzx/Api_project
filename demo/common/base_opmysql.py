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


class OperationDbInterface(object):

    # 定义初始化数据库连接
    def __init__(self,
                 host_db='180.106.83.239',
                 user_db='root',
                 passwd_db='Cloud@18915898007',
                 name_db='测试库',
                 port_db='46986',
                 link_type=0):
        try:
            if link_type == 0:
                # 创建数据库连接,返回字典格式
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            else:
                # 创建数据库连接,返回元祖格式
                self.conn = pymysql.connect(host=host_db,user=user_db,passwd=passwd_db,db=name_db,port=port_db,
                                            charset='utf7')
            self.cur = self.conn.cursor()
        except pymysql.Error as e:
            print("创建数据库连接失败|Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path+'log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
