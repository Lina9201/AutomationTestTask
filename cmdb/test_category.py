import requests
import json
import pytest


def test_api(auth_token):
    url = 'http://172.20.2.118:18081/v1/categories/tree'

    response = requests.get(url)
    print("status code:", response.status_code)

    response_payload = response.json()
    print(response_payload)
    print(response_payload['status'])
    print(response_payload['data'][0])
    print(len(response_payload['data']))

    print(len(response_payload['data'][0]['children']))

    post_url = 'http://172.20.2.118:18081/v1/categories'

    headers = {"User-Agent": "test request headers",
               "content-type": "application/json;charset=UTF-8",
               "authentication": auth_token}

    params = {'key1': 'params1', 'key2': 'params2'}

    data = json.dumps({
      "category": {
        "_key": "447fdcb0e12e4a2395157eab415f4f6f",
        "code": "switch",
        "createTime": "2018-11-29",
        "icon": "iconfont icon-default",
        "modifyTime": "2018-12-20",
        "name": "this is a name",
        "parentCategoryKey": None
      },
      "propGroups": [
        {
          "group": {
            "_key": "447fdcb0e12e4a2395157eab415f4f6f",
            "createTime": "2018-11-29",
            "modifyTime": "2018-12-20",
            "name": "this is a name",
            "type": "menu",
            "weight": 1
          },
          "properties": [
            {
              "_key": "447fdcb0e12e4a2395157eab415f4f6f",
              "code": "name",
              "createTime": "2018-11-29",
              "key": True,
              "modifyTime": "2018-12-20",
              "name": "this is a name",
              "nullable": True,
              "options": [
                {
                  "children": [
                    None
                  ],
                  "code": "supplier/model",
                  "default": True,
                  "name": "Manufacturer Type"
                }
              ],
              "readonly": True,
              "type": "input",
              "unique": True,
              "validateRegex": "string",
              "value": "Region-x",
              "weight": 2
            }
          ]
        }
      ]
    })

    request_payload_json = {
        "category": {
            "_key": "447fdcb0e12e4a2395157eab415f4f6f",
            "code": "switch",
            "createTime": "2018-11-29",
            "icon": "iconfont icon-default",
            "modifyTime": "2018-12-20",
            "name": "this is a name",
            "parentCategoryKey": None
        },
        "propGroups": [
            {
                "group": {
                    "_key": "447fdcb0e12e4a2395157eab415f4f6f",
                    "createTime": "2018-11-29",
                    "modifyTime": "2018-12-20",
                    "name": "this is a name",
                    "type": "menu",
                    "weight": 1
                },
                "properties": [
                    {
                        "_key": "447fdcb0e12e4a2395157eab415f4f6f",
                        "code": "name",
                        "createTime": "2018-11-29",
                        "key": True,
                        "modifyTime": "2018-12-20",
                        "name": "this is a name",
                        "nullable": True,
                        "options": [
                            {
                                "children": [
                                    None
                                ],
                                "code": "supplier/model",
                                "default": True,
                                "name": "Manufacturer Type"
                            }
                        ],
                        "readonly": True,
                        "type": "input",
                        "unique": True,
                        "validateRegex": "string",
                        "value": "Region-x",
                        "weight": 2
                    }
                ]
            }
        ]
    }

    # request_payload_json['category']['name'] = "what the hell is going on?"
    request_payload_json['category']['name'] = ""
    request_payload_json['propGroups'][0]['group']['name'] = "this is a property group name!"
    request_payload_json['propGroups'].append({
                "group": {
                    "_key": "447fdcb0e12e4a2395157eab415f4f6f",
                    "createTime": "2018-11-29",
                    "modifyTime": "2018-12-20",
                    "name": "this is a name",
                    "type": "menu",
                    "weight": 1
                },
                "properties": [
                    {
                        "_key": "447fdcb0e12e4a2395157eab415f4f6f",
                        "code": "name",
                        "createTime": "2018-11-29",
                        "key": True,
                        "modifyTime": "2018-12-20",
                        "name": "this is a name",
                        "nullable": True,
                        "options": [
                            {
                                "children": [
                                    None
                                ],
                                "code": "supplier/model",
                                "default": True,
                                "name": "Manufacturer Type"
                            }
                        ],
                        "readonly": True,
                        "type": "input",
                        "unique": True,
                        "validateRegex": "string",
                        "value": "Region-x",
                        "weight": 2
                    }
                ]
            })

    post_response = requests.post(url=post_url, json=request_payload_json, params=params, headers=headers)
    print("status code:", post_response.status_code)
    print("status code:", post_response.json())
    print(post_response.json()['status'])
    print(len(post_response.json()['data']['propGroups']))

    category_key = post_response.json()['data']['category']['_key']

    del_url = post_url + '/' + category_key

    requests.delete(url=del_url)
    print(category_key, ' deleted!')
    resp = requests.get(url=del_url)
    print(resp.status_code)
    print(resp.json()['status'])
    print(resp.json())

    assert 1


def pytest_generate_tests(metafunc):
    # called once per each test function
    func_arg_list = metafunc.cls.params[metafunc.function.__name__]
    arg_names = sorted(func_arg_list[0])
    metafunc.parametrize(arg_names, [[func_args[name] for name in arg_names] for func_args in func_arg_list])


class TestClass(object):
    # a map specifying multiple argument sets for a test method
    params = {
        'test_equals': [
            dict(a=1, b=2),
            dict(a=3, b=3),
            dict(a=3, b=3),
            dict(a=3, b=3),
            dict(a=3, b=3),
            dict(a=3, b=3),
            dict(a=3, b=3),
        ],
        'test_zero_division': [dict(a=1, b=0), ],
    }

    def test_equals(self, a, b):
        assert a == b

    def test_zero_division(self, a, b):
        with pytest.raises(ZeroDivisionError):
            a / b


if __name__ == '__main__':
    test_api()

