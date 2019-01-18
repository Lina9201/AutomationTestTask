import pytest
import copy
import requests

ip_address_x = 'http://172.20.2.118:18081'
base_url_path = "/v1/categories"
base_url_path_gdp = "/v1/categories/{categoryKey}"
base_url_path_key_properties = "/v1/categories/{categoryKey}/key_properties"
base_url_path_next_to_topo = "/v1/categories/{categoryKey}/next_to_topo"
base_url_path_properties = "/v1/categories/{categoryKey}/properties"
base_url_path_tree = "/v1/categories/tree"
base_url_path_validate_code = "/v1/categories/validate_code"

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


def parametrize_payload(path_to_parameter, value, test_payload=None):
    path_points = path_to_parameter.split('/')
    path_len = len(path_points)

    if test_payload is None:
        test_payload = copy.deepcopy(request_payload_json)

    temp = test_payload
    i = 0
    while i < path_len:
        if i + 1 == path_len:
            temp[path_points[i]] = value
            i = i + 1
        else:
            temp = temp[path_points[i]]
            i = i + 1

    return test_payload


def parametrize_payload_mul(arguments):
    test_payload = copy.deepcopy(request_payload_json)

    for key in arguments:
        parametrize_payload(key, arguments[key], test_payload)

    return test_payload


test_criteria = [
    {'query_values': 'value',  # dictionary
     'payload': parametrize_payload_mul({
         'category/_key': 'id......!',
         'category/code': 'rocking',
         'category/icon': 'icon-font rocking'
        }),
     'response_status_code': '200',
     'response_payload_status': '200',
     'response_payload_snippets': ['icon-font rocking', 'rocking']  # contains strings.
     },
    {'query_values': 'value',  # dictionary
     'payload': parametrize_payload_mul({
         'category/_key': 'id......!',
         'category/code': 'rocking',
         'category/icon': 'icon-font rocking'
        }),
     'response_status_code': '200',
     'response_payload_status': '200',
     'response_payload_snippets': ['icon-font rocking', 'rocking']  # contains strings.
     }
]


@pytest.mark.parametrize("criteria", test_criteria)
def test_create_scenario(ip, port, criteria, headers):
    ip_address = "http://%s:%s" % (ip, port)

    print(criteria)
    query_values = criteria['query_values']
    payload = criteria['payload']
    response_status_code = criteria['response_status_code']
    response_payload_status = criteria['response_payload_status']
    response_payload_snippets = criteria['response_payload_snippets']

    post_response = requests.post(url=ip_address + base_url_path,
                                  json=payload,
                                  params=query_values,
                                  headers=headers)

    assert str(post_response.status_code) == response_status_code
    print("status code:", post_response.status_code)

    resp_payload = post_response.json()
    assert str(resp_payload['status']) == response_payload_status
    print(post_response.json()['status'])

    assert 'data' in resp_payload
    for snippet in response_payload_snippets:
        assert snippet in str(resp_payload)

    # finally, better to remove added.
    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', resp_payload['data']['category']['_key'])
    delete_response = requests.delete(url=url, headers=headers)
    assert delete_response.status_code == 200
