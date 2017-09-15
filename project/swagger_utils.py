import json, requests

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
