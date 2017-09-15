import json
import os
import requests

REST_METHODS = ['get', 'post', 'put', 'delete']

class urlpathnode(object):
    def __init__(self, name, is_full_url=False):
        # the URL segment that this node represents
        self.name = name
        # does the path from the root node to this node represent a complete URL?
        self.is_full_url = is_full_url
        # what REST methods are available on this node?
        self.methods = []
        # what REST methods are available on this node or children of this node?
        self.descendent_methods = []
        # dictionary of child nodes, with node names as keys
        self.children = {}

    def __eq__(self, other_name):
        return other_name == self.name

    def print_node(self, accumulator=""):
        s = "{}{}{} ({}) ({})".format(
            accumulator,
            self.name,
            " (*)" if self.is_full_url else "",
            self.methods,
            self.descendent_methods)
        accumulator += "    "
        for child in self.children.values():
            s += "\n{}".format(child.print_node(accumulator))
        return s

    def add_child_url(self, child_url, methods):
        nodes = child_url.strip("/").split("/")
        self.add_child(nodes, methods)

    def add_child(self, child_url_nodes, methods):
        first, rest = child_url_nodes[0], child_url_nodes[1:]

        # some descendent of this node will have all members of `methods`
        # available, so add all members of `methods` to `descendent_methods`
        self.descendent_methods.extend(methods)
        self.descendent_methods = list(set(self.descendent_methods))

        # find the appropriate child node based on the first URL segment.  If
        # no such child exists, create one
        try:
            child = self.children[first]
        except KeyError as e:
            child = urlpathnode(first)
            self.children[first] = child

        # if there are more child nodes to process, do so recursively
        if rest:
            child.add_child(rest, methods)
        # if we are on the last child node, add the provided `methods` to this
        # node's `methods` list, as well as `descendent_methods` list
        else:
            child.is_full_url = True
            child.methods.extend(methods)
            child.methods = list(set(child.methods))
            child.descendent_methods.extend(methods)
            child.descendent_methods = list(set(child.descendent_methods))

    def get_child_names(self):
        return sorted([child.name for child in self.children])

class urlpathtree(object):
    def __init__(self, swagger_json):
        with open(swagger_json) as f:
            file_data = f.read()

        json_data = json.loads(file_data)

        self.root = urlpathnode("/", False)

        paths = json_data.get("paths")
        for path in paths.keys():
            methods = [method for method in paths[path].keys() if method in REST_METHODS]
            self.root.add_child_url(path, methods)

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
