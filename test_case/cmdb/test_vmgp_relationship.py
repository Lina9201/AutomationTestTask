# -*- coding: utf-8 -*-
# @Time    : 2020/4/9 9:36
# @Author  : zhuxuefei
from common.get_db_data import init_arangodb
import requests
configitem_relationship_url = "admin/v1/relationships/config_item_to_config_item"
def get_configitems():
    """
    获取所有配置项
    :return:
    """
    conn = init_arangodb("cmdb_db")
    arangodb = conn.opendb("cmdb")
    aql = "FOR c IN config_item Filter c.categoryCode=='instance' RETURN c"
    configitems = arangodb.AQLQuery(aql)
    return configitems


def test_vmgp_relationship(uri, headers):
    # configitems = get_configitems()
    # print(type(configitems))
    # print(configitems)
    for configitem in get_configitems():
        create_configitemRelationship_param = [{
            "_to": configitem._key,
            "_from": "12c086595d704289abb9a2a0222aef7e",
            "dictionaryItemKey": "4c2eba9ac031496a938de06a04529591"
        }]

        print(configitem._key)
        create_configitemRelationship_response = requests.post(url=uri + configitem_relationship_url,
                                                               headers=headers,
                                                               json=create_configitemRelationship_param).json()
        # print(create_configitemRelationship_response)
        assert create_configitemRelationship_response['status'] == 200