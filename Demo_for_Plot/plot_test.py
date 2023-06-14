# ============================================================
# Doc Info
# ============================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : plot_test.py
@Time    : 2023/06/20 10:32:18
@Author  : HuJi
@Contact : shootergod@forxmail.com
@Version : 0.1
@Desc    : None
'''


import random
import plot_tools


# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    nums = []
    for _ in range(1000):
        nums.append(random.randint(1, 100))


    plot_tools.bar(data=nums)