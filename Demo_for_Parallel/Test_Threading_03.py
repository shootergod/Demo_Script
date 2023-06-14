# ============================================================
# Doc Info
# ============================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Test_Threading_03.py
@Time    : 2023/06/20 10:29:20
@Author  : HuJi
@Contact : shootergod@forxmail.com
@Version : 0.1
@Desc    : None
'''


import threading
import time


def dowaiting():
    print('    -->> Sub-Threading {} Start ...'.format(
        threading.current_thread().getName()))
    time.sleep(1)
    print('    -->> Sub-Threading {} Finished ...'.format(
        threading.current_thread().getName()))


# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    print('    -->> Main-Threading {} Start ...'.format(
        threading.current_thread().getName()))
    for i in range(9):
        t = threading.Thread(target=dowaiting)
        t.start()

        print('    -->> Main-Threading Do Some Other Things ...')

        # once sub-thread join [to main-thread],
        # main-thread will wait for sub,
        # which means that main prog line# 26 will not be executed.
        t.join()

    print('    -->> Main-Threading {} Finished ...'.format(
        threading.current_thread().getName()))
