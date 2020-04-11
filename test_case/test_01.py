#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:余振新
@file: test_01.py
@time: 2020/04/09
"""
import unittest
from common.base_request import RequestInterface


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_interface = RequestInterface()

    def test_01(self):
        self.test_interface.http_request('', '', '', 'GET')
        self.test_interface.http_request('http://180.106.83.239:18080/apis/login', '', '{\'employeeno\':\'YG3346\',\'pwd\':\'c33367701511b4f6020ec61ded352059\'}', 'POST')
