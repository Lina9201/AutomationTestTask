import copy


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
