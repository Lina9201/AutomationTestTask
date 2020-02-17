# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 21:02
# @Author  : zhuxuefei

import os
from config import Conf
import pytest
from common.get_excel_data import OperationExcleData
import requests
from test_case.cmdb.test_category import get_categorykey
from test_case.cmdb.test_dictionary import get_dictionary
from test_case.cmdb.test_configitems import get_configitem_key
import allure
from utils.LogUtil import my_log


category_relationship_url = "/admin/v1/relationships/category_to_category"
configitem_relationship_url = "admin/v1/relationships/config_item_to_config_item"
testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "配置管理.xlsx"
category_relationship_data = OperationExcleData(excelFile, "配置类型关系").getcase_tuple()
configitem_relationship_data = OperationExcleData(excelFile, "配置项关系").getcase_tuple()

@pytest.mark.cmdb
@pytest.mark.run(order=4)
@allure.feature("CMDB")
@allure.story("创建配置类型间关系")
@pytest.mark.parametrize("ID, testcases, categoryfrom, relationship, categoryto", category_relationship_data)
def test_category_relationship(uri, headers, ID, testcases, categoryfrom, relationship, categoryto):
    """
    创建配置类型间关系
    :param uri:
    :param headers:
    :param ID:
    :param testcases:
    :param categoryfrom:源配置项类型
    :param relationship:关系
    :param categoryto:目的配置项类型
    :return:
    """
    category_from = get_categorykey(categoryfrom)
    category_to = get_categorykey(categoryto)
    relationshipkey = get_dictionary(relationship)
    create_categoryRelationship_param = {
        "_to": category_to,
        "_from": category_from,
        "dictionaryItemKey": relationshipkey._key
    }
    create_categoryRelationship_response = requests.post(url = uri + category_relationship_url,
                                                 headers = headers,
                                                 json= create_categoryRelationship_param).json()
    allure.attach("请求响应code", str(create_categoryRelationship_response['status']))
    allure.attach("请求响应结果", str(create_categoryRelationship_response))
    my_log().info(create_categoryRelationship_response)
    assert create_categoryRelationship_response['status'] == 200

@pytest.mark.cmdb
@pytest.mark.run(order=5)
@allure.feature("CMDB")
@allure.story("创建配置项间关系")
@pytest.mark.parametrize("ID, testcases, fromcode, configitemfrom, relationship, tocode, configitemto", configitem_relationship_data)
def test_configitem_relationship(uri, headers, ID, testcases, fromcode,configitemfrom, relationship, tocode,configitemto):
    """
    创建配置项间关系
    :param uri:
    :param headers:
    :param ID:
    :param testcases:
    :param fromcode:源配置项名称code
    :param configitemfrom:源配置项名称
    :param relationship:关系
    :param tocode:目的配置项名称code
    :param configitemto:目的配置项名称
    :return:
    """
    relationshipkey = get_dictionary(relationship)
    configitem_from = get_configitem_key(fromcode,configitemfrom)
    configitem_to = get_configitem_key(tocode,configitemto)
    create_configitemRelationship_param = [{
        "_to": configitem_to,
        "_from": configitem_from,
        "dictionaryItemKey": relationshipkey._key
    }]
    create_configitemRelationship_response = requests.post(url = uri + configitem_relationship_url,
                                                           headers = headers,
                                                           json =create_configitemRelationship_param).json()
    allure.attach("请求响应code", str(create_configitemRelationship_response['status']))
    allure.attach("请求响应结果", str(create_configitemRelationship_response))
    my_log().info(create_configitemRelationship_response)
    assert create_configitemRelationship_response['status'] == 200



