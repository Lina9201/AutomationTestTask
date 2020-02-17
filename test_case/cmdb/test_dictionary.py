import pytest
import requests
import os
from config import Conf
from common.get_excel_data import OperationExcleData
from common.get_db_data import init_arangodb
import allure
from utils.LogUtil import my_log

#创建、编辑、删除字典url
create_dictionaries_url = "/admin/v1/dictionaries"
update_dictionaries_url="/admin/v1/dictionaries/"
delete_dictionaries_url = "/admin/v1/dictionaries/"
get_parentDictionaryKey_url="/admin/v1/dictionaries/tree"

#获取测试数据
testdata_path=Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "配置管理.xlsx"
create_dictionaries_data=OperationExcleData(excelFile,"创建字典").getcase_tuple()
update_dictionaries_data=OperationExcleData(excelFile,"编辑字典").getcase_tuple()
delete_dictionarie_date=OperationExcleData(excelFile,"删除字典").getcase_tuple()

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


# #根据字典名称查询字典的key值(key=id)
def get_dictionaries_key(dictionaries_name):
    conn=init_arangodb("cmdb_db")
    arangodb=conn.opendb("cmdb")
    aql="FOR c IN dictionary RETURN c"
    queryresult=arangodb.AQLQuery(aql)
    for key in queryresult:
        if key.name == dictionaries_name:
            dictionaries_key=key._key
            return dictionaries_key

# 根据字典名称查询字典的code值
def get_dictionaries_code(dictionaries_name):
    conn=init_arangodb("cmdb_db")
    arangodb=conn.opendb("cmdb")
    aql="FOR c IN dictionary RETURN c"
    queryresult=arangodb.AQLQuery(aql)
    for code in queryresult:
        if code.name == dictionaries_name:
            dictionaries_code=code.code
            return dictionaries_code

#查询父级字典的key值
def get_parent_dictionaries_key(dictionaries_name):
    conn=init_arangodb("cmdb_db")
    arangodb=conn.opendb("cmdb")
    aql="FOR c IN dictionary RETURN c"
    queryresult=arangodb.AQLQuery(aql)
    for key in queryresult:
        if key.name == dictionaries_name:
            parent_dictionaries_key=key.parentDictionaryKey
            return parent_dictionaries_key

#查询父级字典的code值
def get_parent_dictionaries_code(dictionaries_name):
    conn=init_arangodb("cmdb_db")
    arangodb=conn.opendb("cmdb")
    aql="FOR c IN dictionary RETURN c"
    queryresult=arangodb.AQLQuery(aql)
    for code in queryresult:
        if code.name == dictionaries_name:
            parent_dictionaries_code=code.parentDictionaryCode
            return parent_dictionaries_code

#创建一级、二级字典
@pytest.mark.cmdb
@pytest.mark.run(order=6)
@allure.feature("CMDB")
@allure.story("创建字典")
@pytest.mark.parametrize('ID,testcases,dictionaries_name,dictionaries_code,parentDictionary',create_dictionaries_data)
def test_create_dictionaries(uri,headers,ID,testcases,dictionaries_name,dictionaries_code,parentDictionary):
    parentDictionaryKey = get_dictionaries_key(parentDictionary)
    parentDictionaryCode=get_dictionaries_code(parentDictionary)
    create_dictionaries_param={
        'name':dictionaries_name,
        'code':dictionaries_code,
        'properties':{'reverseName': ""},
        'parentDictionaryKey':parentDictionaryKey,
        'parentDictionaryCode':parentDictionaryCode
    }
    create_dictionaries_response=requests.post(url=uri+create_dictionaries_url,
                                               headers=headers,json=create_dictionaries_param).json()
    code=create_dictionaries_response['status']
    allure.attach("请求响应code", str(create_dictionaries_response['status']))
    allure.attach("请求响应结果", str(create_dictionaries_response))
    assert code == 200

#编辑一级、二级字典
@pytest.mark.cmdb
@pytest.mark.run(order=7)
@allure.feature("CMDB")
@allure.story("编辑字典")
@pytest.mark.parametrize('ID,testcases,dictionaries_name,update_dictionaries_name',update_dictionaries_data)
def test_update_dictionaries(uri,headers,ID,testcases,dictionaries_name,update_dictionaries_name):
    DictionaryKey=get_dictionaries_key(dictionaries_name)
    DictionaryCode=get_dictionaries_code(dictionaries_name)
    parentDictionaryKey=get_parent_dictionaries_key(dictionaries_name)
    parentDictionaryCode=get_parent_dictionaries_code(dictionaries_name)
    update_dictionaries_param={
        'name':update_dictionaries_name,
        'code':DictionaryCode,
        'properties':{'reverseName': ""},
        'parentDictionaryKey':parentDictionaryKey,
        'parentDictionaryCode':parentDictionaryCode
    }
    update_dictionaries_response=requests.put(url=uri+update_dictionaries_url+str(DictionaryKey),
                                              headers=headers,json=update_dictionaries_param).json()
    code=update_dictionaries_response['status']
    allure.attach("请求响应code", str(update_dictionaries_response['status']))
    allure.attach("请求响应结果", str(update_dictionaries_response))
    my_log().info(update_dictionaries_response)
    assert code == 200

#删除字典
@pytest.mark.cmdb
@pytest.mark.run(order=8)
@allure.feature("CMDB")
@allure.story("删除字典")
@pytest.mark.parametrize("ID,testcases,dictionaries_name",delete_dictionarie_date)
def test_delete_dictionaries(uri, headers,ID,testcases,dictionaries_name):
    DictionaryKey=get_dictionaries_key(dictionaries_name)
    delete_dictionaries_response = requests.delete(
        url=uri + delete_dictionaries_url + str(DictionaryKey),
        headers=headers
    ).json()
    code = delete_dictionaries_response["status"]
    allure.attach("请求响应code", str(delete_dictionaries_response['status']))
    allure.attach("请求响应结果", str(delete_dictionaries_response))
    assert code == 200