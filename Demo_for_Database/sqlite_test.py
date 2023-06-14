# ============================================================
# Doc Info
# ============================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : sqlite_test.py
@Time    : 2023/06/20 10:27:37
@Author  : HuJi
@Contact : shootergod@forxmail.com
@Version : 0.1
@Desc    : None
'''

# ============================================================
# Import
# ============================================================
import os
import sys

import sqlite3
from typing import Union

# ============================================================
# Constant
# ============================================================
ScriptPath = os.path.abspath(__file__)
ScriptDir = os.path.dirname(ScriptPath)


# ============================================================
# db_generic_operation: frame work of db operation
# ============================================================
def db_generic_operation(db_path: str = None,
                         sql: Union[str, list] = None,
                         mode: str = 'w',
                         info: str = '',
                         rst=None) -> None:
    try:
        # 1st: create db connetion
        conn = sqlite3.connect(db_path)
        # 2nd: get cursor
        cursor = conn.cursor()
        # 3rd: do some sql sentence
        if isinstance(sql, str):
            cursor.execute(sql)
        elif isinstance(sql, list):
            # if it's a list, sentence by sentence
            for item in sql:
                cursor.execute(item)
        else:
            pass
        
        if mode == 'w':
            # case for add, del, modify
            # must commit to apply any changes
            conn.commit()
        elif mode == 'r':
            # case for query
            rst = cursor.fetchall()

    except Exception as e:
        print(e)
        # if error, goto the last status
        conn.rollback()
        #
        print(' --> commit failed: {} @ {}'.format(info, db_path))
    finally:
        # 4th: release the cursor
        cursor.close()
        # 5th: release the connection
        conn.close()
        # show some info
        print(' --> commit successfully: {}'.format(info))

        return rst


# ============================================================
# db_init: create the empty table
# ============================================================
def db_init(db_path):
    sql = "create table user (id int(11) primary key, name varchar(50))"
    info = "db init"
    mode = "w"
    db_generic_operation(db_path=db_path, sql=sql, mode=mode, info=info)


# ============================================================
# db_add_records
# ============================================================
def db_add_records(db_path):
    sql = [
        "insert into user (id,name) values ('1', 'ZSF')",
        "insert into user (id,name) values ('2', 'ZWJ')",
        "insert into user (id,name) values ('3', 'LHC')",
        "insert into user (id,name) values ('4', 'RYY')"
    ]
    info = "db add some records"
    mode = "w"
    db_generic_operation(db_path=db_path, sql=sql, mode=mode, info=info)

# ============================================================
# db_add_records
# ============================================================
def db_query_records(db_path):
    sql = "select * from user"
    info = "db query some records"
    mode = "r"
    rst = db_generic_operation(db_path=db_path, sql=sql, mode=mode, info=info)
    return rst

# ============================================================
# db_modify_records
# ============================================================
def db_modify_records(db_path):
    sql = "update user set name='MMTME' where id=4"
    info = "db modify one of the records"
    mode = "w"
    db_generic_operation(db_path=db_path, sql=sql, mode=mode, info=info)

# ============================================================
# db_delete_records
# ============================================================
def db_delete_records(db_path):
    sql = "delete from user where id=3"
    info = "db delete one of the records"
    mode = "w"
    db_generic_operation(db_path=db_path, sql=sql, mode=mode, info=info)



# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    # do some preparation before db operation
    db_fn = 'test.db'
    db_path = os.path.join(ScriptDir, db_fn)
    if os.path.isfile(db_path):
        os.remove(db_path)

    # init test
    db_init(db_path=db_path)

    # add test
    db_add_records(db_path=db_path)

    # query test
    rst = db_query_records(db_path=db_path)
    print(rst)

    db_modify_records(db_path=db_path)

    # query again to check the change
    rst = db_query_records(db_path=db_path)
    print(rst)

    # del test
    db_delete_records(db_path=db_path)

    # query again to check the change
    rst = db_query_records(db_path=db_path)
    print(rst)





