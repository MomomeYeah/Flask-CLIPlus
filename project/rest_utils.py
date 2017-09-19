import json, requests

CRUD_METHODS = ['get', 'create', 'update', 'delete']
REST_METHODS = ['get', 'post', 'put', 'delete']

def crud_to_rest(crud_method):
    if crud_method not in CRUD_METHODS:
        return None

    index = CRUD_METHODS.index(crud_method)
    return REST_METHODS[index]

def rest_to_crud(rest_method):
    if rest_method not in REST_METHODS:
        return None

    index = REST_METHODS.index(rest_method)
    return CRUD_METHODS[index]

def rest_methods_to_crud(rest_method_list):
    return [
        rest_to_crud(i)
        for i in rest_method_list]

def rest_call_from_tokens(host, port, tokens):
    if tokens:
        method, rest = tokens[0], tokens[1:]
        suffix = "/".join(rest)
        url = "http://{}:{}/{}/".format(host, port, suffix)

        print "Calling URL {}".format(url)

        headers = {
            "Content-Type": "application/json"
        }
        data = {}

        if method in CRUD_METHODS:
            method = REST_METHODS[CRUD_METHODS.index(method)]

        if method not in REST_METHODS:
            return requests.get("http://{}:{}".format(host, port))

        if method == "get":
            return requests.get(url)

        if method == "post":
            return requests.post(url=url, headers=headers, json=data)

        if method == "put":
            return requests.put(url=url, headers=headers, json=data)

        if method == "delete":
            return requests.delete(url=url)

    return requests.get("http://{}:{}".format(host, port))

def print_rest_api_response(response):
    if response.status_code in [200, 201, 204, 400]:
        try:
            print "{}".format(json.dumps(response.json(), indent=4, sort_keys=True))
        except ValueError as e:
            print response.text
    elif response.status_code == 404:
        print "Invalid URL"
    else:
        print response.text
