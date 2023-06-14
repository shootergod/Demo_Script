# ============================================================
# Doc Info
# ============================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Test_Threading_02.py
@Time    : 2023/06/20 10:29:14
@Author  : HuJi
@Contact : shootergod@forxmail.com
@Version : 0.1
@Desc    : None
'''


import threading


def show(num):
    print("Thread %s is running ..." % num)


# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=show, args=(i, ))
        t.start()