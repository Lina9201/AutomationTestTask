# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 20:38
# @Author  : zhuxuefei

from common.get_db_data import init_arangodb


def get_dictionary(dictionaryName):
    """
    查询cmdb数据库根据传入的字段名称获取对应记录
    :param dictionaryName: 字典名称
    :return:
    """
    # 初始化Arangodb数据库对象
    conn = init_arangodb("cmdb_db")
    arangodb = conn.opendb("cmdb")
    aql = "FOR c IN dictionary RETURN c"
    queryresult = arangodb.AQLQuery(aql)
    for dict in queryresult:
        if dict.name == dictionaryName:
            return dict