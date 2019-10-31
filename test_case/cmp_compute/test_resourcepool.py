import pytest
import requests
import json
import os
from config import Conf
from common.get_excel_data import OperationExcleData
from test_case.cmp_compute.test_datacenter import get_datacenterid

# 添加资源池请求url
createResourcePool_url = "/admin/v1/resourcepools"

testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "资源池.xlsx"
sheetName = "添加资源池"
resourcepool_data = OperationExcleData(excelFile, sheetName).getcase_tuple()

@pytest.mark.parametrize("ID,testcases,regionname,name,type,descrption,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version", resourcepool_data)
def test_createResourcePool(uri, headers,ID,testcases, regionname,name,type,descrption,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version):
    """
    添加资源池接口
    :param ip:
    :param port:
    :param headers:
    :param resourcepool_data:
    :return:
    """
    create_vcresourcepool_data = {
        "region": get_datacenterid(uri, headers, regionname),
        "name": name,
        "type": type,
        "extra":{
            "datacenter": datacenter
        },
        "ip": rpip,
        "port": rpport,
        "proxyIp": proxyIp,
        "proxyPort": proxyPort,
        "username": username,
        "password": password
    }

    create_opresourcepool_data = {
         "region": get_datacenterid(uri, headers, regionname),
         "name": name,
         "type": type,
         "extra": {
             "version": version,
             "region": region,
             "domain": domain,
             "projectId": projectId,
             "protocol": protocol
         },
         "ip": rpip,
         "port": rpport,
         "proxyIp": proxyIp,
         "proxyPort": proxyPort,
         "username": username,
         "password": password
    }

    if type == "vmware":
        createvcResourcePool_response = requests.post(url=uri + createResourcePool_url,
                                              data=json.dumps(create_vcresourcepool_data),
                                              headers=headers)
        code = createvcResourcePool_response.status_code
        assert code == 200
        print(createvcResourcePool_response.text)
    elif type == "openstack":
        createvcResourcePool_response = requests.post(url=uri + createResourcePool_url,
                                                      data=json.dumps(create_opresourcepool_data),
                                                      headers=headers)
        code = createvcResourcePool_response.status_code
        assert code == 200
        print(createvcResourcePool_response.text)


if __name__ == '__main__':
        pytest.main()




