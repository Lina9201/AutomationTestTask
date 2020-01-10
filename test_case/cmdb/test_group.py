# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 18:36
# @Author  : zhuxuefei
from common.get_db_data import init_arangodb


def get_group(groupName):
    """
    查询cmdb数据库根据传入的配置项类型group获取对应记录
    :param groupName:
    :return:
    """
    # 初始化Arangodb数据库对象
    conn = init_arangodb("cmdb_db")
    arangodb = conn.opendb("cmdb")
    aql = "FOR c IN group RETURN c"
    queryresult = arangodb.AQLQuery(aql)
    for group in queryresult:
        if group.name == groupName:
            return group