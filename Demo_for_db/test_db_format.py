# ============================================================
# Doc Info
# ============================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : test_db_format.py
@Time    : 2023/09/15 09:05:30
@Author  : HuJi
@Contact : shootergod@forxmail.com
@Version : 0.1
@Desc    : None
'''

# ============================================================
# Import
# ============================================================
import os, csv

import logging, time, datetime

# ============================================================
# Constant
# ============================================================
CWD = os.path.dirname(__file__)
REG = 'reg'


TS = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S.%f')

LOG_FN = 'log_' + TS + '.txt'
LOG_FP = os.path.join(CWD, 'log',  LOG_FN)

# ============================================================
# Log Prepare
# ============================================================
# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='demo.log', level=logging.DEBUG)
logging.basicConfig(filename=LOG_FP, filemode='w', level=logging.DEBUG)

# ============================================================
# Functions
# ============================================================


def __is_bit_set(num: int, bp: int):
    # bit pos checking
    # bp: bit pos from right
    return num & (1 << bp - 1)


def __csv_reader(fp: str) -> dict:
    with open(file=fp, mode='r', encoding='utf-8') as fid:
        lines = csv.reader(fid)
        rst = {int(line[0]): line[1:] for line in lines}
    return rst


def __get_analysis_type(code: int) -> list[str]:
    return ANALYSIS_TYPE[code]


def __get_device_type(code: int) -> list[str]:
    device_types = []
    if code == 0:
        device_types.append(DEVICE_TYPE[0][0])
    else:
        for i in range(3):
            bp = i + 1
            if __is_bit_set(code, bp):
                device_types.append(DEVICE_TYPE[bp][0])
    return device_types


def approach_code(code: int):

    tmp_analysis_code = code // 10
    tmp_device_code = code % 10

    analysis_type = __get_analysis_type(tmp_analysis_code)
    device_types = __get_device_type(tmp_device_code)

    logging.debug('-' * 60)
    logging.debug('approach_code: {}'.format(code))
    logging.debug(' -> analysis_code: {}'.format(tmp_analysis_code))
    logging.debug(analysis_type)
    logging.debug(' -> device_code: {}'.format(tmp_device_code))
    logging.debug(device_types)


def __get_table_type(code: int) -> list[str]:
    return TABLE_TYPE[code]


def __get_data_format_type(code: int) -> list[str]:
    bp = 1
    if __is_bit_set(code, bp):
        return DATA_FORMAT[bp]
    else:
        return DATA_FORMAT_C[bp]


def __get_sort_type(code: int) -> list[str]:
    bp = 2
    if __is_bit_set(code, bp):
        return SORT_TYPE[bp]
    else:
        return SORT_TYPE_C[bp]


def __get_random_type(code: int) -> list[str]:
    bp = 3
    if __is_bit_set(code, bp):
        return RANDOM_TYPE[bp]
    else:
        return RANDOM_TYPE_C[bp]


def table_code(code: int):

    tmp_table_type_code = code % 1000
    tmp_other_3_codes = code // 1000

    table_type = __get_table_type(tmp_table_type_code)

    data_format = __get_data_format_type(tmp_other_3_codes)
    sort_type = __get_sort_type(tmp_other_3_codes)
    random_type = __get_random_type(tmp_other_3_codes)

    logging.debug('-' * 60)
    logging.debug('table_code: {}'.format(code))
    logging.debug(' -> table_type_code: {}'.format(tmp_table_type_code))
    logging.debug(table_type)
    logging.debug(' -> data_format_code: {}'.format(tmp_other_3_codes))
    logging.debug(data_format)
    logging.debug(' -> sort_type_code: {}'.format(tmp_other_3_codes))
    logging.debug(sort_type)
    logging.debug(' -> random_type_code: {}'.format(tmp_other_3_codes))
    logging.debug(random_type)


# ============================================================
# reg
# ============================================================
ANALYSIS_TYPE = __csv_reader(os.path.join(CWD, REG,  'd_analysis_type.csv'))
DEVICE_TYPE = __csv_reader(os.path.join(CWD, REG,  'b_device_type.csv'))

DATA_FORMAT = __csv_reader(os.path.join(CWD, REG,  'b_data_format.csv'))
DATA_FORMAT_C = __csv_reader(os.path.join(CWD, REG,  'b_data_format_c.csv'))

SORT_TYPE = __csv_reader(os.path.join(CWD, REG,  'b_sort_type.csv'))
SORT_TYPE_C = __csv_reader(os.path.join(CWD, REG,  'b_sort_type_c.csv'))

RANDOM_TYPE = __csv_reader(os.path.join(CWD, REG,  'b_random_type.csv'))
RANDOM_TYPE_C = __csv_reader(os.path.join(CWD, REG,  'b_random_type_c.csv'))

TABLE_TYPE = __csv_reader(os.path.join(CWD, REG,  'd_table_type.csv'))

# ============================================================
# Test
# ============================================================

if __name__ == '__main__':

    # for i in range(10):
    #     approach_code(i+1)


    approach_code(1)
    # approach_code(61)
    # approach_code(15)
    # approach_code(106)

    # table_code(4)
    # table_code(14)
    # table_code(5)
    # table_code(1005)
    # table_code(2010)
    # table_code(3005)
    # table_code(5003)

    # table_code(1)
