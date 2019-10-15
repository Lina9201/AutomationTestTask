import pytest
import requests
def test_createdb():
    # ip_address=ip+port
    ip_address = 'http://172.50.10.42:8000'

    other_url = '/admin/v1/regions'

    # url=ip_address
    url = ip_address + other_url

    # 参数/消息体
    param = {'name': "dxy",'description': "dxy"}

    #消息头
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://172.50.10.42',
        'Referer': 'http://172.50.10.42/console/',
        'T-AUTH-TOKEN': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJiZmZiOTdjMy02NTQxL' \
                        'TQxY2QtYmI5Ny1jMzY1NDE0MWNkYjYiLCJzdWIiOiJkdXhpYW5neXUiLCJpYXQiOjE1Nj' \
                        'gwMDUxMDAsImlzcyI6IkFwYWNoZVN5bmNvcGUiLCJleHAiOjE1NjgwMTk1MDAsIm5iZiI6MTU' \
                        '2ODAwNTEwMH0.gfjguTuTaHpQdAMqwMWJtJecMLacbjq0ufQii6VQktfRcnCYugtScJp5P' \
                        '2-Jq9H3mRxnTUilD6U3064cYO24ew',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 '\
        }

    #消息体
    createdb_request=requests.post(url=url,json=param ,headers=headers)

    #将request请求.json转化成json格式，其实就是response响应值
    createdb_response = createdb_request.json()

    #提取响应值中status值code代码为200
    code = createdb_response['status']

    name = createdb_response['data']['name']

    #进行断言assert
    assert code==200

    #调用创建用户中心发送参数来判断param['name']
    assert name==param['name']

