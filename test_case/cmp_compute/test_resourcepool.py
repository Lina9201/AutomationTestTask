import pytest
import requests
import json
from common.get_excel_data import OperationExcleData
from test_case.cmp_compute.test_datacenter import test_get_datacenterid

# 添加资源池请求url
createResourcePool_url = "/admin/v1/resourcepools"

excelFile = "E:\\AutomationTestTask\\data\\cmp\\资源池.xlsx"
sheetName = "添加资源池"
resourcepool_data = OperationExcleData(excelFile, sheetName).getCaseList(excelFile, sheetName)

def test_getDataCenterRegion(ip, port, headers):
    """
    获取创建的数据中心的region，并写入到添加资源池的sheet页测试用例对应字段中
    :param ip:
    :param port:
    :param headers:
    :return:
    """
    regionID = test_get_datacenterid(ip, port, headers)
    OperationExcleData(excelFile, sheetName).writeExcel(excelFile, sheetName, regionID)

@pytest.mark.parametrize("resourcepool_data", resourcepool_data)
def test_createResourcePool(ip, port, headers,resourcepool_data):
    """
    添加资源池接口
    :param ip:
    :param port:
    :param headers:
    :param resourcepool_data:
    :return:
    """
    ip_address = "http://%s:%s" % (ip, port)
    createResourcePool_response = requests.post(url=ip_address + createResourcePool_url,
                                              data=json.dumps(resourcepool_data),
                                              headers=headers)
    code = createResourcePool_response.status_code
    assert code == 200
    print(createResourcePool_response.text)

if __name__ == '__main__':
        pytest.main()




