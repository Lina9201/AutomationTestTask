import pytest
import copy
import requests

base_url_path = "/v1/categories"
base_url_path_gdp = "/v1/categories/{categoryKey}"
base_url_path_key_properties = "/v1/categories/{categoryKey}/key_properties"
base_url_path_next_to_topo = "/v1/categories/{categoryKey}/next_to_topo"
base_url_path_properties = "/v1/categories/{categoryKey}/properties"
base_url_path_tree = "/v1/categories/tree"
base_url_path_validate_code = "/v1/categories/validate_code"

json_category_basic = {
    "_key": "447fdcb0e12e4a2395157eab415f4f6f",
    "code": "switch",
    "createTime": "2018-11-29",
    "icon": "iconfont icon-default",
    "modifyTime": "2018-12-20",
    "name": "this is a name",
    "parentCategoryKey": None
}

json_property = {
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

json_property_group = {
    "_key": "447fdcb0e12e4a2395157eab415f4f6f",
    "createTime": "2018-11-29",
    "modifyTime": "2018-12-20",
    "name": "this is a name",
    "type": "menu",
    "weight": 1
}

json_category = {
    "category": json_category_basic,
    "propGroups": [
        {
            "group": json_property_group,
            "properties": [
                json_property,
            ]
        },
        {
            "group": json_property_group,
            "properties": [
                json_property,
            ]
        },
    ]
}


def parametrize_payload(payload_json, path_to_parameter, value):
    if payload_json is None:
        raise Exception("Function: parametrize_payload_mul, Parameter: payload_json is none.")

    path_points = path_to_parameter.split('/')
    path_len = len(path_points)

    temp = payload_json
    i = 0
    while i < path_len:
        if i + 1 == path_len:
            temp[path_points[i]] = value
            i = i + 1
        else:
            temp = temp[path_points[i]]
            i = i + 1

    return payload_json


def parametrize_payload_mul(payload_json, arguments):
    if payload_json is None:
        raise Exception("Function: parametrize_payload_mul, Parameter: payload_json is none.")

    test_payload = copy.deepcopy(payload_json)

    for key in arguments:
        parametrize_payload(test_payload, key, arguments[key])

    return test_payload


test_create_criteria = [
    {'query_strings': 'value',  # dictionary
     'payload': parametrize_payload_mul(json_category, {
         'category/_key': 'id......!',
         'category/code': 'rocking',
         'category/icon': 'icon-font rocking',
         'category/icon': 'icon-font rocking',
     }),
     'response_status_code': '200',
     'response_payload_status': '200',
     'response_payload_snippets': ['icon-font rocking',
                                   'rocking']  # contains strings.
     },

    {'query_strings': 'value',  # dictionary
     'payload': parametrize_payload_mul(json_category, {
         'category/_key': 'what is the id!',
         'category/code': 'shaking',
         'category/icon': 'icon-font shaking'
     }),
     'response_status_code': '200',
     'response_payload_status': '200',
     'response_payload_snippets': [
         'icon-font shaking',
         'shaking']  # contains strings.
     },

    {'query_strings': 'value',  # dictionary
     'payload': parametrize_payload_mul(json_category, {
         'category/_key': 'what is the id!',
         'category/code': 'shaking',
         'category/icon': 'icon-font shaking',
         'propGroups': None,
     }),
     'response_status_code': '200',
     'response_payload_status': '200',
     'response_payload_snippets': [
         'icon-font shaking',
         'shaking']  # contains strings.
     }
]

test_update_criteria = [
    {'query_strings': 'value',  # dictionary
     'payload': parametrize_payload_mul(json_category_basic, {
         '_key': 'id......!',
         'code': 'rocking',
         'icon': 'icon-font rocking'
     }),
     'response_status_code': '200',
     'response_payload_status': '200',
     'response_payload_snippets': ['icon-font rocking',
                                   'rocking']  # contains strings.
     },
    {'query_strings': 'value',  # dictionary
     'payload': parametrize_payload_mul(json_category_basic, {
         '_key': 'id......!',
         'code': 'rocking',
         'icon': 'icon-font rocking'
     }),
     'response_status_code': '200',
     'response_payload_status': '200',
     'response_payload_snippets': ['icon-font rocking',
                                   'rocking']  # contains strings.
     },
    {'query_strings': 'value',  # dictionary
     'payload': parametrize_payload_mul(json_category_basic, {
         '_key': 'what is the id!',
         'code': 'shaking',
         'icon': 'icon-font shaking',
         'propGroups': None
     }),
     'response_status_code': '200',
     'response_payload_status': '200',
     'response_payload_snippets': [
         'icon-font shaking',
         'shaking']  # contains strings.
     }
]


@pytest.mark.parametrize("criteria", test_create_criteria)
def test_create_scenario(ip, port, criteria, headers):
    ip_address = "http://%s:%s" % (ip, port)

    print(criteria)
    query_values = criteria['query_strings']
    payload = criteria['payload']
    response_status_code = criteria['response_status_code']
    response_payload_status = criteria['response_payload_status']
    response_payload_snippets = criteria['response_payload_snippets']

    # create new category.
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

    category_key = resp_payload['data']['category']['_key']

    # verify the category exists.
    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
    get_response = requests.get(url=url, headers=headers)
    assert get_response.status_code == requests.status_codes.codes.OK

    resp_payload = get_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    assert 'data' in resp_payload
    for snippet in response_payload_snippets:
        assert snippet in str(resp_payload)

    # finally, better to remove the created.
    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
    delete_response = requests.delete(url=url, headers=headers)
    assert delete_response.status_code == requests.status_codes.codes.OK


@pytest.mark.parametrize("criteria", test_update_criteria)
def test_update_scenario(ip, port, criteria, headers):
    ip_address = "http://%s:%s" % (ip, port)
    print(criteria)
    query_values = criteria['query_strings']
    payload = criteria['payload']
    response_status_code = criteria['response_status_code']
    response_payload_status = criteria['response_payload_status']
    response_payload_snippets = criteria['response_payload_snippets']

    # create new category.
    post_response = requests.post(url=ip_address + base_url_path,
                                  json=json_category,
                                  params=query_values,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.

    category_key = resp_payload['data']['category']['_key']

    # update created category.
    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
    put_response = requests.put(url=url,
                                json=payload,
                                params=query_values,
                                headers=headers)
    assert str(put_response.status_code) == response_status_code
    resp_payload = put_response.json()
    assert str(resp_payload['status']) == response_payload_status  # to be defined.
    assert 'data' in resp_payload
    for snippet in response_payload_snippets:
        assert snippet in str(resp_payload)

    # verify the category exists.
    get_response = requests.get(url=url, params=query_values, headers=headers)
    assert get_response.status_code == requests.status_codes.codes.OK

    resp_payload = get_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    assert 'data' in resp_payload
    for snippet in response_payload_snippets:
        assert snippet in str(resp_payload)

    # finally, better to remove the created.
    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
    delete_response = requests.delete(url=url, headers=headers)
    assert delete_response.status_code == requests.status_codes.codes.OK


@pytest.mark.parametrize("criteria", test_update_criteria)
def test_crud10_scenario(ip, port, criteria, headers):
    ip_address = "http://%s:%s" % (ip, port)
    query_values = criteria['query_strings']
    payload = criteria['payload']
    response_status_code = criteria['response_status_code']
    response_payload_status = criteria['response_payload_status']
    response_payload_snippets = criteria['response_payload_snippets']

    category_keys = []
    category = copy.deepcopy(json_category)

    # create 10 new category.
    for x in range(0, 10):
        category_name = 'category_' + str(x)
        post_response = requests.post(url=ip_address + base_url_path,
                                      json=parametrize_payload(category, 'category/name', category_name),
                                      headers=headers)

        assert post_response.status_code == requests.status_codes.codes.OK
        resp_payload = post_response.json()
        assert resp_payload['status'] == 200  # to be defined.
        category_key = resp_payload['data']['category']['_key']
        category_keys.append(category_key)

        url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
        get_response = requests.get(url=url, headers=headers)
        assert get_response.status_code == requests.status_codes.codes.OK
        resp_payload = get_response.json()
        assert resp_payload['status'] == 200  # to be defined.
        print(resp_payload)
        assert resp_payload['data']['name'] == category_name

    for category_key in category_keys:
        # update 10
        url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
        put_response = requests.put(url=url,
                                    json=payload,
                                    params=query_values,
                                    headers=headers)
        assert str(put_response.status_code) == response_status_code
        resp_payload = put_response.json()
        assert str(resp_payload['status']) == response_payload_status  # to be defined.
        assert 'data' in resp_payload
        for snippet in response_payload_snippets:
            assert snippet in str(resp_payload)

        # finally, better to remove the created.
        url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
        delete_response = requests.delete(url=url, headers=headers)
        assert delete_response.status_code == requests.status_codes.codes.OK
        resp_payload = get_response.json()
        assert resp_payload['status'] == 200  # to be defined.

        # verify whether deleted.
        url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
        get_response = requests.get(url=url, headers=headers)
        assert get_response.status_code == requests.status_codes.codes.OK
        resp_payload = get_response.json()
        assert resp_payload['status'] == 200  # to be defined.
        print(resp_payload)
        assert 'data' not in resp_payload


def test_exceptions_scenario(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    # create new category.
    post_response = requests.post(url=ip_address + base_url_path,
                                  json=json_category,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    category_key = resp_payload['data']['category']['_key']

    # try to query category not existing.
    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', 'Not existing')
    get_response = requests.get(url=url, headers=headers)
    assert get_response.status_code == requests.status_codes.codes.OK  # ???

    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
    get_response = requests.get(url=url, headers=headers)
    assert get_response.status_code == requests.status_codes.codes.OK

    # try to delete category not existing.
    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', 'Not existing')
    delete_response = requests.delete(url=url, headers=headers)
    assert delete_response.status_code == requests.status_codes.codes.OK

    url = (ip_address + base_url_path_gdp).replace('{categoryKey}', category_key)
    delete_response = requests.delete(url=url, headers=headers)
    assert delete_response.status_code == requests.status_codes.codes.OK


def test_query_tree_scenario(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)

    # create 1st category.
    post_response = requests.post(url=ip_address + base_url_path,
                                  json=json_category,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    category_key = resp_payload['data']['category']['_key']
    first_key = category_key

    # create 2nd category.
    post_response = requests.post(url=ip_address + base_url_path,
                                  json=parametrize_payload(json_category, 'category/parentCategoryKey', category_key),
                                  headers=headers)
    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    category_key = resp_payload['data']['category']['_key']
    second_key = category_key

    # create 3rd category.
    post_response = requests.post(url=ip_address + base_url_path,
                                  json=parametrize_payload(json_category, 'category/parentCategoryKey', category_key),
                                  headers=headers)
    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    category_key = resp_payload['data']['category']['_key']
    third_key = category_key

    url = ip_address + base_url_path_tree
    get_response = requests.get(url=url, headers=headers)
    assert get_response.status_code == requests.status_codes.codes.OK
    resp_payload = get_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    assert 'data' in resp_payload
    assert len(resp_payload['data']) > 0
    print(resp_payload['data'])

    error_flag = True
    for category in resp_payload['data']:
        if category['id'] == first_key:
            error_flag = False
            assert category['leaf'] is False
            assert category['isParent'] is True
            assert len(category['children']) > 0
            for child in category['children']:
                if child['id'] == second_key:
                    error_flag = False
                    assert child['leaf'] is False
                    assert child['isParent'] is True
                    assert child['parentId'] == first_key
                    assert len(child['children']) > 0
                    for sub_child in child['children']:
                        if sub_child['id'] == third_key:
                            error_flag = False
                            assert sub_child['leaf'] is True
                            assert sub_child['isParent'] is False
                            assert sub_child['parentId'] == second_key
                            assert len(sub_child['children']) == 0

    assert error_flag is False
