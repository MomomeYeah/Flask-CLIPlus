import json, re, requests

CRUD_METHODS = ['get', 'create', 'update', 'delete']
REST_METHODS = ['get', 'post', 'put', 'delete']

# convert a CRUD method to REST
def crud_to_rest(crud_method):
    if crud_method not in CRUD_METHODS:
        return None

    index = CRUD_METHODS.index(crud_method)
    return REST_METHODS[index]

# convert a REST method to CRUD
def rest_to_crud(rest_method):
    if rest_method not in REST_METHODS:
        return None

    index = REST_METHODS.index(rest_method)
    return CRUD_METHODS[index]

# convert a list of REST methods to a corresponding list of CRUD methods
def rest_methods_to_crud(rest_method_list):
    return [
        rest_to_crud(i)
        for i in rest_method_list]

# given a list of tokens, separate it into two lists:
#  - those that correspond to segments of a URL
#  - those that correspond to POST/PUT parameters
#
# parameters are considered to be strings of the form xxx=yyy
def separate_url_segments_from_params(tokens):
    url_segments = []
    params = []

    param_pattern = re.compile("^.*=.*$")
    for token in tokens:
        if param_pattern.match(token):
            params.append(token)
        else:
            url_segments.append(token)

    return url_segments, params

# given a list of POST/PUT parameters of the form xxx=yyy, return a dictionary
# suitable for use as POST/PUT data, e.g. { xxx: yyy }
#
# if the same param is specified more than once, the last value specified
# will win
def create_params_dic(params):
    dic = {}
    for param in params:
        key, val = param.split("=")
        dic[key] = val

    return dic

def rest_call_from_tokens(host, port, tokens):
    if tokens:
        method, rest = tokens[0], tokens[1:]
        url_segments, params = separate_url_segments_from_params(rest)
        params = create_params_dic(params)
        suffix = "/".join(url_segments)
        url = "http://{}:{}/{}/".format(host, port, suffix)

        print "Calling URL {}".format(url)
        print "With params {}".format(params)

        headers = {
            "Content-Type": "application/json"
        }

        if method in CRUD_METHODS:
            method = REST_METHODS[CRUD_METHODS.index(method)]

        if method not in REST_METHODS:
            print "Invalid method {} - defaulting to GET".format(method)
            return requests.get("http://{}:{}".format(host, port))

        if method == "get":
            print "Using method GET"
            return requests.get(url)

        if method == "post":
            print "Using method POST"
            return requests.post(url=url, headers=headers, json=params)

        if method == "put":
            print "Using method PUT"
            return requests.put(url=url, headers=headers, json=params)

        if method == "delete":
            print "Using method DELETE"
            return requests.delete(url=url)

    print "No tokens specified - using method GET"
    return requests.get("http://{}:{}".format(host, port))

def print_rest_api_response(response):
    print "response code is {}".format(response.status_code)
    if response.status_code in [200, 201, 400]:
        try:
            print "{}".format(json.dumps(response.json(), indent=4, sort_keys=True))
        except ValueError as e:
            print "Invalid response"
    # deletion results in status code 204 which should have no content
    elif response.status_code == 204:
        print "Deletion successful"
    # 404 can either be URL not found, or an error message, as JSON
    elif response.status_code == 404:
        try:
            print json.dumps(response.json(), indent=4, sort_keys=True)
        except ValueError as e:
            print "Invalid URL"
    else:
        print response.text
