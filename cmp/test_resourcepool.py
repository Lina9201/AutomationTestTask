import pytest
import requests

creat_url_path = "/v1/resourcepools"
#check_url = "/v1/resourcepools/{resourcePoolId}"
#update_url = "/v1/resourcepools/{resourcePoolId}"
connect_url = "/v1/resourcepools/connecttesting"
update_password_url = "/v1/resourcepools/{resourcePoolId}/password"

param = [{"region": 27287673.829845935,
  "name": "cillum",
  "type": "irure est aute",
  "ip": "sit laboris id aliqua cill",
  "port": 38639636.718895346,
  "username": "",
  "password": "dolor",
  "extra": {
    "datacenter": "esse officia occaecat et velit",
    "region": "qui nostrud",
    "protocal": "nulla sed tempor occaecat",
    "domain": "cupidatat"}}
]

update_param = [{
  "region": 1,
  "name": "deserunt enim",
  "description": "sed ullamco occaecat",
  "ip": "adipisicing in anim aute",
  "port": 15445532.754962876,
  "proxyIp": "consequat dolore velit reprehenderit Ut",
  "proxyPort": -91655201.5879195,
  "username": "sit Excepteur ut voluptate qui"
}]

update_password = [{
  "password": "ut"
}]

connect=[{
  "type": "aute qui aliqua",
  "ip": "inci",
  "port": -69663434.88071649,
  "username": "est",
  "password": "esse dolor dolore est consequat",
  "extra": {}
}
]

@pytest.mark.parametrize("createparam",param)
@pytest.mark.parametrize("updateparam",update_param)

def test_resourcepool(ip, port, createparam,updateparam, headers):
    ip_address = "http://%s:%s" % (ip, port)

    print(createparam)
    # query_values = createparam['query_strings']
    # payload = createparam['payload']
    #response_status_code = createparam['response_status_code']
    #response_payload_status = createparam['response_payload_status']
    # response_payload_snippets = createparam['response_payload_snippets']

    # 创建资源池
    create_post_response = requests.post(url=ip_address + creat_url_path,
                                  params=createparam,
                                  headers=headers).json()
    code = create_post_response["data"]["status"]
    resource_id = create_post_response["data"]["id"]

    #print(create_post_response)
    try:
        assert code == 200#response_status_code
    except Exception as e:
        raise e
    #return resource_id
    # 查询资源池
    check_url = "/v1/resourcepools/%resourceId" %resource_id
    check_response = requests.get(url=ip_address + check_url,
                                  headers = headers).json()
    code = check_response["data"]["status"]
    #print(check_response)
    try:
        assert code == 200#response_status_code
    except Exception as e:
        raise e

    #修改资源池
    update_response = requests.put(url=ip_address + check_url,
                                   params = updateparam,
                                  headers = headers).json()
    #code = update_response["data"]["status"]
    name = updateparam["name"]
    check_response = requests.get(url=ip_address + check_url,
                                  headers=headers).json()
    code = check_response["data"]["status"]
    update_name = check_response["data"]["name"]#修改名称
    print(update_response)
    try:
        assert code == 200 # response_status_code
        assert update_name == name
    except Exception as e:
        raise e

    # 修改资源池密码
    update_password_url = "/v1/resourcepools/ %resource_id/password" %resource_id
    update_response = requests.put(url=ip_address + update_password_url,
                                       params=updateparam,
                                       headers=headers).json()
    # code = update_response["data"]["status"]
    name = updateparam["name"]
    check_response = requests.get(url=ip_address + check_url,
                                      headers=headers).json()
    code = check_response["data"]["status"]
    update_name = check_response["data"]["name"]  # 修改名称
    print(update_response)
    try:
        assert code == 200  # response_status_code
        assert update_name == name
    except Exception as e:
        raise e


#查询资源池连接
@pytest.mark.parametrize("connectparam", connect)
def test_connect(ip, port, connectparam, headers):
    ip_address = "http://%s:%s" % (ip, port)


    connect_response = requests.put(url=ip_address + connect_url,
                                   params=connectparam,
                                   headers=headers).json()
    code = connect_response["data"]["status"]
    try:
        assert code == 200 # response_status_code
    except Exception as e:
        raise e





