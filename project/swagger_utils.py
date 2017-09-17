import json, requests

# given the host and port name of a swagger server, and a full file path to
# save to, grab the swagger.json file from the server, and save it to the
# given path
def get_swagger_api_definition(host, port, file_path):
    api_url = "http://{}:{}/swagger.json".format(host, port)
    swagger_data = requests.get(api_url)

    try:
        swagger_json = swagger_data.json()
    except ValueError as e:
        print "Unable to convert swagger response to JSON"
        exit(1)

    with open(file_path, "w") as f:
        f.write(json.dumps(swagger_json, indent=4, sort_keys=True))

# given the JSON definition of a method for a particular URL, and the
# `definitions` dictionary from the swagger definition, resolve the list of
# parameter names that method accepts
def get_method_body_parameters(method_data, definitions):
    all_parameters = method_data.get("parameters")
    if not all_parameters:
        return None

    # the parameters we're interested in are the payload parameters, where the
    # `in` value is `body`
    body_parameters = [
        param for param in all_parameters
        if param.get("in") == "body"]

    # if no such parameters exist, or somehow we found more than one set,
    # return None
    if len(body_parameters) != 1:
        return None

    param = body_parameters[0]
    schema = param.get("schema")

    if not schema:
        return None

    ref = schema.get("$ref")
    if not ref:
        return None

    definition_name = ref.lstrip("#/definitions")
    param_value = definitions.get(definition_name)
    if not param_value:
        return None

    param_properties = param_value.get("properties")
    if not param_properties:
        return None

    keys = param_properties.keys()
    return keys
