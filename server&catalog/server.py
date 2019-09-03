import pytest
import requests
import tcrc.function.tenant
import tcrc.common.ssh

server_url = "/admin/v1/services"
key_url = "/v1//processes/key"
remind_url = "/admin/v1//service/vps/remind-way"
operation_url = "/admin/v1//service/vps/expired-operation"
datacenter_url = "/admin/v1//regions"
resourcepool_url = "/admin/v1//resourcepools"
image_url = "/admin/v1//images"


# 审批流程选择“流程选择”需要获取流程，选择默认是不用获取
def key(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    key_response = requests.get(url=ip_address + key_url,
                                headers=headers)
    key_response_2 = key_response.json()
    code = key_response_2["status"]
    assert code == 200
    key = key_response_2["data"][0]["key"]
    process_name = key_response_2["data"][0]["name"]
    return key, process_name

# 获取提醒方式
def remind(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    remind_response = requests.get(url=ip_address + remind_url,
                                   headers=headers)
    remind_response_2 = remind_response.json()
    code = remind_response_2["status"]
    assert code == 200
    # print(remind_response_2)
    remind_way = remind_response_2["data"][0]["value"]
    return remind_way

#获取过期操作
def operation(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    operation_response = requests.get(url=ip_address + operation_url,
                                      headers=headers)
    operation_response_2 = operation_response.json()
    code = operation_response_2["status"]
    assert code == 200
    # print(operation_response_2)
    operation = operation_response_2["data"][0]["value"]
    return operation

# 获取数据中心
def datacenter(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    datacenter_response = requests.get(url=ip_address + datacenter_url,
                                       headers=headers)
    datacenter_response_2 = datacenter_response.json()
    code = datacenter_response_2["status"]
    assert code == 200
    # print(datacenter_response_2)
    datacenter_id = datacenter_response_2["data"][1]["id"]
    datacenter_name = datacenter_response_2["data"][1]["name"]
    # assert datacenter_response==0
    return datacenter_id, datacenter_name

# 获取资源池
def resourcepool(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    resourcepool_response = requests.get(url=ip_address + resourcepool_url,
                                         headers=headers)
    resourcepool_response_2 = resourcepool_response.json()
    code = resourcepool_response_2["status"]
    assert code == 200
    # print(resourcepool_response_2)
    # 获取所有资源池
    data = resourcepool_response_2["data"]
    # print(data)
    # 获取选择的数据中心下的资源池
    # 获取数据中心
    datacenter_id = datacenter(ip, port, headers)[0]
    list_b = []
    for i in data:
        if i["region"] == datacenter_id:
            list_b.append(i)
    # print(list_b)
    resourcepool_id = list_b[0]["id"]
    resourcepool_name = list_b[0]["name"]
    # assert resourcepool_response_2==0
    # 返回资源池id
    return resourcepool_id, resourcepool_name

# 获取镜像
def image(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    # 获取所选资源池下的镜像
    pool_id = resourcepool(ip, port, headers)[0]
    image_url = "/admin/v1//images?poolIds=%s" %pool_id
    image_response = requests.get(url=ip_address + image_url,
                                  headers=headers)
    image_response_2 = image_response.json()
    code = image_response_2["status"]
    assert code == 200
    # print(image_response_2)
    # 获取镜像id
    data = image_response_2["data"][0]
    image_id = data["id"]
    image_name = data["name"]
    image_type = data["osType"]
    return image_id, image_name, image_type

# 构建创建数据
def create_param(ip, port, headers):
    key_id = key(ip, port, headers)[0]
    process_name = key(ip, port, headers)[1]
    remind_id = remind(ip, port, headers)
    operation_id = operation(ip, port, headers)
    datacenter_id = datacenter(ip, port, headers)[0]
    datacenter_name = datacenter(ip, port, headers)[1]
    pool_id = resourcepool(ip, port, headers)[0]
    pool_name = resourcepool(ip, port, headers)[1]
    image_id = image(ip, port, headers)[0]
    image_name = image(ip, port, headers)[1]
    image_type = image(ip, port, headers)[2]
    tenant = tcrc.function.tenant.test_check(ip, port, headers)[0]

    create_param = {"serviceType":"VPS",
                    "serviceContent":{
                        "vmType":"vmware","vmTypeLabel":"VMware","processName":process_name,"processKey":key_id, "name":"TEST123","opening":0,"description":"","catalogId":"","accessIds":[tenant],
                        "remind":{"remindDays":1,"frequency":"onetime","remindWay":remind_id,"remindTime":"09:54:23"},
                        "expiredPolicies":[{"expiredDays":1,"operation":operation_id}],
                        "location":[{"infrastructurename":pool_name,"resourceId":pool_id,"identity":datacenter_id,"name":datacenter_name}],
                        "choseOsTypes":["Linux","Windows"],"vmSize":"20",
                        "cpuMenSpecifs":[{"cpuSize":"1","memorySize":"1","unit":"day","fee":"1","valid":True,"repeat":False}],"maxDiskSize":1,
                        "diskSpecif":{"diskCapacity":1,"diskSize":1,"fee":"1","unit":"day"},
                        "osSpecifs":[{"fee":"1","unit":"day","identity":image_id,"osName":image_name,"osCategory":image_type,"isHidden":False,"checked":True}],
                        "bandwidthSpecifs":[{"size":"1","unit":"day","fee":"1"}]}}
    # print(create_param)
    # assert create_param==0
    return create_param

# 构建编辑数据，编辑描述
def update_param(ip, port, headers):
    key_id = key(ip, port, headers)[0]
    process_name = key(ip, port, headers)[1]
    remind_id = remind(ip, port, headers)
    operation_id = operation(ip, port, headers)
    datacenter_id = datacenter(ip, port, headers)[0]
    datacenter_name = datacenter(ip, port, headers)[1]
    pool_id = resourcepool(ip, port, headers)[0]
    pool_name = resourcepool(ip, port, headers)[1]
    image_id = image(ip, port, headers)[0]
    image_name = image(ip, port, headers)[1]
    image_type = image(ip, port, headers)[2]
    tenant = tcrc.function.tenant.test_check(ip, port, headers)[0]

    update_param = {"serviceType":"VPS",
                    "serviceContent":{
                        "vmType":"vmware","vmTypeLabel":"VMware","processName":process_name,"processKey":key_id, "name":"TEST123","opening":0,"description":"dfsggg","catalogId":"","accessIds":[tenant],
                        "remind":{"remindDays":1,"frequency":"onetime","remindWay":remind_id,"remindTime":"09:54:23"},
                        "expiredPolicies":[{"expiredDays":1,"operation":operation_id}],
                        "location":[{"infrastructurename":pool_name,"resourceId":pool_id,"identity":datacenter_id,"name":datacenter_name}],
                        "choseOsTypes":["Linux","Windows"],"vmSize":"20",
                        "cpuMenSpecifs":[{"cpuSize":"1","memorySize":"1","unit":"day","fee":"1","valid":True,"repeat":False}],"maxDiskSize":1,
                        "diskSpecif":{"diskCapacity":1,"diskSize":1,"fee":"1","unit":"day"},
                        "osSpecifs":[{"fee":"1","unit":"day","identity":image_id,"osName":image_name,"osCategory":image_type,"isHidden":False,"checked":True}],
                        "bandwidthSpecifs":[{"size":"1","unit":"day","fee":"1"}]}}
    # print(create_param)
    # assert create_param==0
    return update_param

#上线版本描述
v_description = {"versionDescription":"1"}

# 创建服务
def test_create_server(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    param = create_param(ip, port, headers)
    create_response = requests.post(url=ip_address + server_url,
                                    json=param,
                                    headers=headers)
    create_response_2 = create_response.json()
    code = create_response_2["status"]
    assert code == 200
    # print(create_response_2)
    # 创建时输入的名称
    create_name = param["serviceContent"]["name"]
    # print(create_name)
    # 创建后列表第一条记录的名称
    real_name = test_check(ip, port, headers)[1]
    # print(real_name)
    assert create_name == real_name

# 查询列表
def test_check(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    check_response = requests.get(url=ip_address + server_url,
                                  headers=headers)
    check_response_2 = check_response.json()
    code = check_response_2["status"]
    # print(check_response_2)
    assert code == 200
    data =check_response_2["data"][0]
    id = data["id"]
    name = data["name"]
    description = data["description"]
    serviceStatus = data["serviceStatus"]
    return id, name, description, serviceStatus

# 编辑名称
def test_update_server(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    param = update_param(ip, port, headers)
    server_id = test_check(ip, port, headers)[0]
    update_url = "/admin/v1/services/%s" % server_id
    print(update_url)
    update_response = requests.put(url=ip_address + update_url,
                                   json=param,
                                   headers=headers)
    update_response_2 = update_response.json()
    code = update_response_2["status"]
    assert code == 200
    print(update_response_2)
    # 创建时输入的描述
    create_description = param["serviceContent"]["description"]
    # 编辑时输入的描述
    update_description = param["serviceContent"]["description"]
    # print(update_description)
    # 创建后列表第一条记录的描述
    real_description = test_check(ip, port, headers)[2]
    # print(real_name)
    assert update_description == real_description
    assert create_description != real_description

# 查看详情
def test_detail(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    detail_response = requests.get(url=ip_address + server_url,
                                   headers=headers)
    detail_response_2 = detail_response.json()
    code = detail_response_2["status"]
    # print(detail_response_2)
    assert code == 200
    # 详情中的名称、描述
    detail_name = detail_response_2["data"][0]["name"]
    # print(detail_name)
    detail_description = detail_response_2["data"][0]["description"]
    # print(detail_description)
    # 列表中的名称、描述
    name = test_check(ip, port, headers)[1]
    # print(name)
    description = test_check(ip, port, headers)[2]
    # print(description)
    assert detail_name == name
    assert detail_description == description

# 上线
def test_publish(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    server_id = test_check(ip, port, headers)[0]
    publish_url = "/admin/v1/services/%s/publish" % server_id
    publish_response = requests.post(url=ip_address + publish_url,
                                     json=v_description,
                                     headers=headers)
    # publish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    publish_time = tcrc.common.ssh.transtime()
    # print(publish_time)
    publish_response_2 = publish_response.json()
    code = publish_response_2["status"]
    assert code ==200
    # print(publish_response_2)
    #发布后的状态
    status = test_check(ip, port, headers)[3]
    assert status == 1
    return publish_time

#下线
def test_offline(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    server_id = test_check(ip, port, headers)[0]
    offline_url = "/admin/v1/services/%s/offline" % server_id
    offline_response = requests.post(url=ip_address + offline_url,
                                     headers=headers)
    # offline_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    offline_time = tcrc.common.ssh.transtime()
    # print(offline_time)
    offline_response_2 = offline_response.json()
    code = offline_response_2["status"]
    assert code ==200
    # print(offline_response_2)
    #发布后的状态
    status = test_check(ip, port, headers)[3]
    assert status == 0
    return offline_time

#查看发布历史版本
def test_history(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    server_id = test_check(ip, port, headers)[0]
    history_url = "/admin/v1/services/%s/history" % server_id
    delete_response1 = requests.get(url=ip_address + history_url ,
                                      headers=headers)
    delete_response_2 = delete_response1.json()
    data = delete_response_2["data"]
    code = data["status"]
    publish_time = data[0]["publishTime"]
    offline_time = data[0]["modifiedTime"]
    # print(data)
    assert code == 200
    assert publish_time == test_publish(ip, port, headers)
    assert offline_time == test_offline(ip, port, headers)


#删除服务
def test_delete(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    server_id = test_check(ip, port, headers)[0]
    delete_url = "/admin/v1/services/%s" % server_id
    delete_response = requests.delete(url=ip_address + delete_url,
                                     headers=headers)
    delete_response_2 = delete_response.json()
    code = delete_response_2["status"]
    assert code == 200
    # print(delete_response_2)
    #删除后的id
    after_id = test_check(ip, port, headers)[0]
    assert server_id !=after_id

if __name__ == '__main__':
    pytest.main(['-q', 'server.py'])