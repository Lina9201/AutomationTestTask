# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 9:36
# @Author  : zhuxuefei
import os
from config import Conf
import pytest
from common.get_excel_data import OperationExcleData
import requests
from test_case.cmdb.test_category import get_category_code
from test_case.cmdb.test_group import get_group
from test_case.cmdb.test_property import get_property
from common.get_db_data import init_arangodb
import allure
from utils.LogUtil import my_log
from utils.AssertUtil import AssertUtil

# 配置项url
base_configitems_url = "/admin/v1/config_items"
testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "配置管理.xlsx"
category_data = OperationExcleData(excelFile, "创建配置项").getcase_tuple()
update_category_data = OperationExcleData(excelFile, "编辑配置项").getcase_tuple()
delete_category_data = OperationExcleData(excelFile, "删除配置项").getcase_tuple()

@pytest.mark.cmdb
@pytest.mark.run(order=3)
@allure.feature("CMDB")
@allure.story("创建配置项")
@pytest.mark.parametrize("ID, testcases,category,groupname,propertyname,propertycode,propertvalue,status_code,expected_result", category_data)
def test_create_configitems(uri, headers,ID, testcases,category,groupname,propertyname,propertycode,propertvalue,status_code,expected_result):
   """
   创建配置项
   :param uri:
   :param headers:
   :param ID:
   :param testcases:
   :param category:
   :param groupname:
   :param propertyname:
   :param propertycode:
   :param propertvalue:
   :return:
   """
   categoryCode = get_category_code(category)
   group = get_group(groupname)
   property = get_property(propertycode, propertyname)
   create_configitems_param = {
       "configItem": {
           "categoryCode": categoryCode,
           "name": ""
       },
       "propGroups": [{
           "group": {
               "_key": group._key,
               "name": groupname,
               "deleted": group.deleted,
               "type": "tab",
               "important":group.important,
               "weight": group.weight,
               "code": group.code,
           },
           "properties": [{
               "_key": property._key,
               "name": propertyname,
               "deleted": property.deleted,
               "code": propertycode,
               "type": property.type,
               "value": propertvalue,
               "encrypt": property.encrypt,
               "readonly": property.readonly,
               "nullable": property.nullable,
               "unique": property.unique,
               "key": property.key,
               "important": property.important,
               "builtIn": property.builtIn,
               "weight": property.weight,
               "regex": property.regex,
           }
           ]
       }]
    }

   create_configitems_response = requests.post(
       url=uri + base_configitems_url,
       headers=headers,
       json=create_configitems_param
   ).json()
   allure.attach("请求响应code", str(create_configitems_response['status']))
   allure.attach("请求响应结果", str(create_configitems_response))
   my_log().info(create_configitems_response)
   assert create_configitems_response['status'] == 200
   AssertUtil().assert_code(create_configitems_response['status'],status_code)
   AssertUtil().assert_in_body(create_configitems_response['data'],expected_result)

@pytest.mark.cmdb
@pytest.mark.run(order=6)
@allure.feature("CMDB")
@allure.story("编辑配置项")
@pytest.mark.parametrize("ID, testcases,category,groupname,propertyname,propertycode,propertvalue,updatevlaue,status_code,expected_result", update_category_data)
def test_update_configitems(uri, headers,ID, testcases,category,groupname,propertyname,propertycode,propertvalue,updatevlaue,status_code,expected_result):
    """
    编辑配置项
    :param uri:
    :param headers:
    :param ID:
    :param testcases:
    :param category:
    :param groupname:
    :param propertyname:
    :param propertycode:
    :param propertvalue:
    :return:
    """
    categoryCode = get_category_code(category)
    group = get_group(groupname)
    property = get_property(propertycode, propertyname)
    update_configitems_param = {
        "configItem": {
            "categoryCode": categoryCode,
            "name": ""
        },
        "propGroups": [{
            "group": {
                "_key": group._key,
                "name": groupname,
                "deleted": group.deleted,
                "type": "tab",
                "important": group.important,
                "weight": group.weight,
                "code": group.code,
            },
            "properties": [{
                "_key": property._key,
                "name": propertyname,
                "deleted": property.deleted,
                "code": propertycode,
                "type": property.type,
                "value": updatevlaue,
                "encrypt": property.encrypt,
                "readonly": property.readonly,
                "nullable": property.nullable,
                "unique": property.unique,
                "key": property.key,
                "important": property.important,
                "builtIn": property.builtIn,
                "weight": property.weight,
                "regex": property.regex,
            }
            ]
        }]
    }
    configitem = get_configitem_key(propertycode,propertvalue)
    update_configitems_response = requests.put(url = uri + base_configitems_url + "/" + configitem,
                                            headers = headers,
                                            json = update_configitems_param).json()
    allure.attach("请求响应code", str(update_configitems_response['status']))
    allure.attach("请求响应结果", str(update_configitems_response))
    my_log().info(update_configitems_response)
    AssertUtil().assert_code(update_configitems_response['status'], status_code)
    AssertUtil().assert_in_body(update_configitems_response['data'], expected_result)

@pytest.mark.cmdb
@pytest.mark.run(order=7)
@allure.feature("CMDB")
@allure.story("删除配置项")
@pytest.mark.parametrize("ID, testcases,namecode,configitem,status_code", delete_category_data)
def test_delete_configitem(uri, headers,ID, testcases,namecode,configitem,status_code):
    """
    删除配置项接口
    :param uri:
    :param headers:
    :param ID:
    :param testcases:
    :param namecode:
    :param configitem:
    :return:
    """
    configitem = get_configitem_key(namecode, configitem)
    delete_configitem_response = requests.delete(url = uri + base_configitems_url + "/" + configitem,
                                                 headers = headers,
                                                 ).json()
    allure.attach("请求响应code", str(delete_configitem_response['status']))
    allure.attach("请求响应结果", str(delete_configitem_response))
    my_log().info(delete_configitem_response)
    AssertUtil().assert_code(delete_configitem_response['status'], status_code)
    assert configitem not in get_configitems()


def get_configitems():
    """
    获取所有配置项
    :return:
    """
    conn = init_arangodb("cmdb_db")
    arangodb = conn.opendb("cmdb")
    aql = "FOR c IN config_item RETURN c"
    configitems = arangodb.AQLQuery(aql)
    return configitems

def get_configitem_key(propertyCode,itemName):
    """
    查询cmdb数据库根据传入的配置项名称获取对应记录的_key值
    :param itemName:
    :return:
    """
    configitems = get_configitems()
    for configitem in configitems:
        if configitem.property['%s' % propertyCode] == itemName:
            return configitem._key

