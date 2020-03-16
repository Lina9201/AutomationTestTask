# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 10:18
# @Author  : zhuxuefei
from config.Conf import ConfigYaml
from utils.MysqlUtil import MysqlUtil
from utils.ArangodbUtil import ArangodbUtil
from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log
import allure

def init_mysqldb(db_alias):
    # 从配置文件读取数据库信息进行初始化
    db_info = ConfigYaml().get_db_config(db_alias)
    db_host = db_info["db_host"]
    db_user = db_info["db_user"]
    db_password = db_info["db_password"]
    db_name = db_info["db_name"]
    db_charset = db_info["db_charset"]
    db_port = int(db_info["db_port"])

    conn = MysqlUtil(db_host, db_user, db_password, db_name, db_charset, db_port)
    return conn

def init_arangodb(db_alias):
    #从配置文件中读取Arangodb数据库信息进行初始化
    arangodb_info = ConfigYaml().get_db_config(db_alias)
    arangoURL = arangodb_info['arangoURL']
    username = arangodb_info['username']
    password = arangodb_info['password']

    conn = ArangodbUtil(arangoURL, username,password)
    return conn

def assert_mysqldb(excepted_db,db_res):
    """
    mysql数据库结果与接口返回的结果验证
    :param db_name:
    :param result:
    :param db_verify:
    :return:
    """
    assert_util = AssertUtil()
    for line in excepted_db.keys():
        try:
            excepted_line = excepted_db[line]
            res_db_line = dict(db_res)[line]
            assert_util.assert_body(excepted_line, res_db_line)
            return True
        except:
            my_log("DBUtil").error("数据库断言error, 数据库查询结果 is %s,期望数据库字段 is %s" % (db_res, excepted_db))
            allure.attach("数据库断言error, 数据库查询结果 is %s,期望数据库字段 is %s" % (db_res, excepted_db))
            raise


if __name__ == "__main__":
    sql = init_mysqldb("tcrc_db")
    resourcepool = "vmware资源池"
    sql_query = "select id,name from bizops_tenant.resourcepool where name='%s' " % resourcepool
    print(sql_query)
    db_res = sql.fetchone(sql_query)
    print(db_res)
    # verify_list = list(dict(db_res).keys())
    # excepted_db = {'id':104}
    # assert_mysqldb("tcrc_db", excepted_db, "select id,name from bizops_tenant.resourcepool where name='vmware资源池' ")








