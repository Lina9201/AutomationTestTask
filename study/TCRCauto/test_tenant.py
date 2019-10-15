import pytest
import requests

#url_path
vdc_url_path = '/admin/v1/vdcs'


#测试数据
vdc_list = [{"name": "du1", "description": "备注"},{"name": "du2", "description": "备注"}]
vdc_listname=[]
for i in vdc_list:
    vdc_listname.append(i["name"])
vdc_updatename=[]
for i in vdc_listname:
    vdc_updatename.append((i,i+"1"))
vdc_deletename=[]
for i in vdc_listname:
    vdc_deletename.append(i+"1")



#构造函数
#租户id
def search_vdcid(ip,port,headers,vdc_listname):
    ip_address = 'http://%s:%s'%(ip, port)
    vdc_request = requests.get(url = ip_address+vdc_url_path,headers=headers)
    vdcid_response = vdc_request.json()
    vdcdata = vdcid_response['data']

    for i in vdcdata:
        if i['name'] in vdc_listname:
            return i['id']
    return 0


#测试用例
#创建租户
@pytest.mark.parametrize('param',vdc_list)
def test_create_vdc(ip,port,headers,param):
    ip_address = 'http://%s:%s' % (ip, port)
    create_vdc_reques = requests.post(url = ip_address+vdc_url_path,json=param,headers=headers)
    create_vdc_response = create_vdc_reques.json()
    assert create_vdc_response['status'] == 200


#通过租户名，搜索租户
@pytest.mark.parametrize('vdc_name',vdc_listname)
def test_search_vdc(ip,port,headers,vdc_name):
    assert search_vdcid(ip, port, headers,vdc_name) != 0

@pytest.mark.parametrize('vdc_name,update_vdc_name',vdc_updatename)
def test_update_vdc(ip,port,headers,vdc_name,update_vdc_name):
    ip_address = "http://%s:%s"%(ip,port)
    id = str(search_vdcid(ip,port,headers,vdc_name))
    param = {"id":id,"name":update_vdc_name,"description":""}
    update_vdc_request = requests.post(url=ip_address+vdc_url_path+'/'+id,json=param,headers=headers)
    update_vdc_response = update_vdc_request.json()
    print(update_vdc_response)
    assert update_vdc_response["status"]==200

#删除租户
@pytest.mark.parametrize('vdc_name',vdc_deletename)
def test_delete_vdc(ip,port,headers,vdc_name):
    ip_address = 'http://%s:%s' % (ip, port)
    id = str(search_vdcid(ip,port,headers,vdc_name))
    delete_vdc_request = requests.delete(url = ip_address+vdc_url_path+'/'+id,headers=headers)
    delete_vdc_response = delete_vdc_request.json()
    print(delete_vdc_response)

    assert delete_vdc_response['status'] == 200
    assert search_vdcid(ip, port, headers,vdc_name) == 0
