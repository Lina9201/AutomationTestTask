# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 9:36
# @Author  : zhuxuefei
from common.get_db_data import init_mysqldb
if __name__=="__main__":
    db = init_mysqldb('tcrc_db')
    print(db)
