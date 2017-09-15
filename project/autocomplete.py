import os

from swagger_utils import get_swagger_api_definition
from urlpathtree import urlpathtree

CRUD_METHODS = ['get', 'create', 'update', 'delete']
REST_METHODS = ['get', 'post', 'put', 'delete']

class autocomplete(object):
    def __init__(self):
        # get API definition
        swagger_filename = "swagger.json"
        json_path = os.path.join(
            os.path.dirname(__file__),
            swagger_filename)

        get_swagger_api_definition("localhost", "5123", json_path)

        # generate path tree
        self.path_tree = urlpathtree(swagger_filename)
        print str(self.path_tree)

    def find_node(self, node, tokens):
        num_tokens = len(tokens)

        # if we have no tokens to match, no match
        if num_tokens == 0:
            return None

        # find all children of the current node that match the next token
        child_nodes = node.find_matching_children(tokens[0])

        # if we're on the last token, return children of the current node
        if num_tokens == 1:
            return child_nodes

        # otherwise, loop through all children and create a list of all their
        # matching descendent nodes
        nodes = []
        for child_node in child_nodes:
            grandchildren = self.find_node(child_node, tokens[1:])
            if grandchildren:
                nodes.extend(grandchildren)

        # return all nodes that we found
        return nodes

    def find_node_from_root(self, tokens):
        if not tokens:
            return None

        # seed self.find_node with the path tree root node
        return self.find_node(self.path_tree.root, tokens)

if __name__ == "__main__":
    ac = autocomplete()

    token_tests= [
        ["books", "2"],
        ["authors"],
        ["authors", "1"],
        ["authors", "1", "publications"],
        ["authors", "1", "mismatch"],
    ]

    for test in token_tests:
        nodes = ac.find_node_from_root(test)

        print "for {}, nodes are:".format(test)
        for node in nodes:
            print str(node)
