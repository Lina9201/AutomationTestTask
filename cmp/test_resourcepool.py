import pytest
import requests
import json
from Common.get_excel_data import OperationExcleData
from cmp.test_datacenter import test_getDataCenterId

# 添加资源池请求url
createResourcePool_url = "/admin/v1/resourcepools"

excelFile = "E:\\AutomationTestTask\\Test_data\\计算资源\\资源池.xlsx"
sheetName = "添加资源池"
resourcepool_data = OperationExcleData(excelFile, sheetName).getCaseList(excelFile, sheetName)

def getDataCenterRegion(ip, port, headers):
    regionID = test_getDataCenterId(ip, port, headers)
    OperationExcleData(excelFile, sheetName).writeExcel(excelFile, sheetName, regionID)

@pytest.mark.parametrize("resourcepool_data", resourcepool_data)
def test_createResourcePool(ip, port, headers, resourcepool_data):
    ip_address = "http://%s:%s" % (ip, port)
    createResourcePool_response = requests.post(url=ip_address + createResourcePool_url,
                                              data=json.dumps(resourcepool_data),
                                              headers=headers)
    code = createResourcePool_response.status_code
    assert code == 200
    print(createResourcePool_response.text)




