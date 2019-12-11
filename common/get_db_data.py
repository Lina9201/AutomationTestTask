# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 10:18
# @Author  : zhuxuefei
from config.Conf import ConfigYaml
from utils.MysqlUtil import MysqlUtil
from utils.AssertUtil import AssertUtil

def init_db(db_alias):
    # 从配置文件读取数据库信息进行初始化
    db_info = ConfigYaml.get_db_config(db_alias)
    db_host = db_info["db_host"]
    db_user = db_info["db_user"]
    db_password = db_info["db_password"]
    db_name = db_info["db_name"]
    db_charset = db_info["db_charset"]
    db_port = int(db_info["db_port"])

    conn = MysqlUtil(db_host, db_user, db_password, db_name, db_charset, db_port)
    return conn


def assert_db(db_name,result,db_verify):
    assert_util = AssertUtil()
    sql = init_db(db_name)
    db_res = sql.fetchone(db_verify)
    verify_list = list(dict(db_res).keys())
    for line in verify_list:
        res_line = result[line]
        res_db_line = dict(db_res)[line]
        assert_util.assert_body(res_line, res_db_line)
