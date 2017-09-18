import json, requests

REST_METHODS = ['get', 'post', 'put', 'delete']

def rest_call_from_tokens(host, port, tokens):
    suffix = "/".join(tokens)
    url = "http://{}:{}/{}".format(host, port, suffix)

    r = requests.get(url)
    return r

def print_rest_api_response(response):
    try:
        print "{}".format(json.dumps(response.json(), indent=4, sort_keys=True))
    except ValueError as e:
        print "Unable to decode JSON object"
