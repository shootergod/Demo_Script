# ============================================================
# Doc Info
# ============================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : TestMyCase1.py
@Time    : 2023/06/20 10:34:59
@Author  : HuJi
@Contact : shootergod@forxmail.com
@Version : 0.1
@Desc    : None
'''


import unittest

class TestMyCase1(unittest.TestCase):
    def setUp(self):
        print("-----> setup")

    def tearDown(self):
        print("—-—-—> teardown")

    def test_1(self):
        print("T1 testl")

    def test_2(self):
        print("T1 test2")

    def test_3(self):
        print("T1 test3")

    def test_4(self):
        print("T1 test4")

if __name__ == '__main__':
    unittest.main()