import json
import os
import requests

class urlpathnode(object):
    def __init__(self, name, is_full_url=False):
        self.name = name
        self.is_full_url = is_full_url
        self.children = {}

    def __eq__(self, other_name):
        return other_name == self.name

    def print_node(self, accumulator=""):
        s = "{}{}{}".format(accumulator, self.name, " (*)" if self.is_full_url else "")
        accumulator += "    "
        for child in self.children.values():
            s += "\n{}".format(child.print_node(accumulator))
        return s

    def add_child_url(self, child_url):
        nodes = child_url.strip("/").split("/")
        self.add_child(nodes)

    def add_child(self, child_url_nodes):
        first, rest = child_url_nodes[0], child_url_nodes[1:]
        try:
            child = self.children[first]
        except KeyError as e:
            child = urlpathnode(first)
            self.children[first] = child

        if rest:
            child.add_child(rest)
        else:
            child.is_full_url = True

    def get_child_names(self):
        return sorted([child.name for child in self.children])

class urlpathtree(object):
    def __init__(self, swagger_json):
        with open(swagger_json) as f:
            file_data = f.read()

        json_data = json.loads(file_data)

        self.root = urlpathnode("/", False)
        for path in json_data.get("paths"):
            self.root.add_child_url(path)

        print self.root.print_node()

if __name__ == "__main__":
    # get Swagger JSON from API server
    api_url = "http://localhost:5123/swagger.json"
    swagger_data = requests.get(api_url).json()

    # save as swagger.json
    swagger_filename = "swagger.json"
    json_path = os.path.join(
        os.path.dirname(__file__),
        swagger_filename)

    with open(json_path, "w") as f:
        f.write(json.dumps(swagger_data, indent=4, sort_keys=True))

    # generate path tree
    u = urlpathtree(swagger_filename)
