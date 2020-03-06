# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 18:51
# @Author  : zhuxuefei
import os
from config import Conf
import pytest
from common.get_excel_data import OperationExcleData
import requests
from test_case.cmdb.test_category import get_categorykey
from common.get_db_data import init_arangodb
import allure
from utils.LogUtil import my_log
from utils.AssertUtil import AssertUtil

base_category_url = "/admin/v1/categories"
testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "配置管理.xlsx"
add_property_data = OperationExcleData(excelFile, "修改类型属性").getcase_tuple()


def get_property(propertyCode, propertyName):
    """
    根据属性名称和code获取属性记录
    :param propertyCode:
    :param propertyName:
    :return:
    """
    conn = init_arangodb("cmdb_db")
    arangodb = conn.opendb("cmdb")
    aql = "FOR c IN property RETURN c"
    queryresult = arangodb.AQLQuery(aql)
    for property in queryresult:
        if property.name == propertyName and property.code == propertyCode:
            return property

@pytest.mark.cmdb
@pytest.mark.run(order=2)
@allure.feature("CMDB")
@allure.story("添加配置项类型属性")
@pytest.mark.parametrize("ID, testcases, categoryname, groupname, groupweight, code, name, type, nullable,unique,readonly, key, default, encrypt, weight, status_code, expected_result", add_property_data)
def test_add_property(uri, headers, ID, testcases, categoryname, groupname, groupweight,code, name, type, nullable,unique,readonly, key, default,encrypt, weight,status_code, expected_result):
    add_property_param =[
        {
            "group": {
                "type": "tab",
                "weight": "1",
                "name": "基本信息",
                "important": "true"
            },
            "properties": [{
                "name": "名称",
                "code": "name",
                "type": "input",
                "value": "",
                "readonly": "false",
                "nullable": "false",
                "unique": "true",
                "key": "true",
                "important": "true",
                "weight": "1",
                "validateRegex": "",
                "options": [],
                "properties": {
                    "isBuildInName": "true"
                }
            }, {
                "name": "责任人",
                "code": "administrator",
                "type": "userChoice",
                "value": "",
                "readonly": "false",
                "nullable": "false",
                "unique": "true",
                "key": "false",
                "important": "false",
                "weight": "1",
                "validateRegex": "",
                "options": [],
                "properties": {
                    "isBuildInName": "true"
                }
            }]
        },
        {
            "group": {
                "_key": "",
                "name": groupname,
                "type": "tab",
                "weight": groupweight,
                "tabPopoverShow":"false"
            },
            "properties": [{
                "name": name,
                "code": code,
                "type": type,
                "value": default,
                "encrypt": encrypt,
                "readonly": readonly,
                "nullable": nullable,
                "unique": unique,
                "key": key,
                "users":[],
                "weight": weight,
                # "regex": property.regex,
            }]
        }
    ]

    categorykey = get_categorykey(categoryname)
    add_property_response = requests.put(url = uri + base_category_url + "/" + categorykey + "/properties",
                                        headers = headers,
                                        json = add_property_param
                                        ).json()
    allure.attach("请求响应code", str(add_property_response['status']))
    allure.attach("请求响应结果", str(add_property_response))
    my_log().info(add_property_response)
    AssertUtil().assert_code(add_property_response['status'], status_code)
    AssertUtil().assert_in_body(add_property_response['data'], expected_result)





