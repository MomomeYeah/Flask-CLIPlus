import json, os, re

from rest_utils import REST_METHODS
from swagger_utils import get_swagger_api_definition, get_method_body_parameters

class urlpathnode(object):
    def __init__(self, name, is_full_url=False):
        # the URL segment that this node represents
        self.name = name
        # does the path from the root node to this node represent a complete URL?
        self.is_full_url = is_full_url
        # what REST methods are available on this node?
        self.methods = {}
        # what REST methods are available on this node or children of this node?
        self.descendent_methods = []
        # dictionary of child nodes, with node names as keys
        self.children = {}

    def is_wildcard_node(self):
        pattern = re.compile("^{.+}$")
        if pattern.match(self.name):
            return True

        return False

    def to_string(self, accumulator=""):
        s = "{}{}{} ({}) ({})".format(
            accumulator,
            self.name,
            " (*)" if self.is_full_url else "",
            self.methods,
            self.descendent_methods)
        accumulator += "    "
        for child in self.children.values():
            s += "\n{}".format(child.to_string(accumulator))
        return s

    def __str__(self):
        return self.to_string()

    # given a full URL, split it on slashes and recursively add its segements
    # as URL path nodes
    def add_child_url(self, child_url, methods, definitions):
        nodes = child_url.strip("/").split("/")
        self.add_child(nodes, methods, definitions)

    def add_child(self, child_url_nodes, methods, definitions):
        first, rest = child_url_nodes[0], child_url_nodes[1:]
        method_keys = [method for method in methods]

        # some descendent of this node will have all members of `methods`
        # available, so add all members of `methods` to `descendent_methods`
        self.descendent_methods.extend(method_keys)
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
            child.add_child(rest, methods, definitions)
        # if we are on the last child node, add the provided `methods` to this
        # node's `methods` list, as well as `descendent_methods` list
        else:
            child.is_full_url = True
            child.descendent_methods.extend(method_keys)
            child.descendent_methods = list(set(child.descendent_methods))

            for method, data in methods.iteritems():
                body_parameters = get_method_body_parameters(data, definitions)
                child.methods[method] = body_parameters

    # return all children of the current node whose decendent method list
    # contains the given REST method
    def get_children_having_descendent_method(self, method):
        return sorted([
            name for name, child in self.children.iteritems()
            if method in child.descendent_methods
            ])

    # return all children of the current node that are either wildcard nodes
    # or whose name matches the specified token
    def find_matching_children(self, token):
        matches = [
            child for child in self.children.values()
            if child.is_wildcard_node() or token == child.name]

        return matches

class urlpathtree(object):
    def __init__(self, swagger_json):
        self.root = urlpathnode("/", False)

        try:
            with open(swagger_json) as f:
                file_data = f.read()

            json_data = json.loads(file_data)

            definitions = json_data.get("definitions")
            paths = json_data.get("paths")

            for path in paths.keys():
                methods = {
                    method: data
                    for method, data in paths[path].iteritems()
                    if method in REST_METHODS
                }
                self.root.add_child_url(path, methods, definitions)
        # File DNE
        except IOError as e:
            pass
        # Unable to parse JSON object
        except ValueError as e:
            pass

    def __str__(self):
        return str(self.root)

if __name__ == "__main__":
    swagger_filename = "swagger.json"
    json_path = os.path.join(
        os.path.dirname(__file__),
        swagger_filename)

    get_swagger_api_definition("localhost", "5123", json_path)

    # generate path tree
    u = urlpathtree(swagger_filename)
    print str(u)
