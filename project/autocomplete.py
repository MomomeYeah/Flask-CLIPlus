#!/usr/bin/python

import os, sys

import rest_utils
from rest_utils import CRUD_METHODS, REST_METHODS
from swagger_utils import get_swagger_api_definition
from urlpathtree import urlpathtree

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

    # Called from find_node_from_root - find node from tokens recursively
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

    # given a list of tokens, find the URL path node that these tokens
    # represent in the URL path tree, based on matching individual tokens with
    # successive nodes
    def find_node_from_root(self, tokens):
        if not tokens:
            return [self.path_tree.root]

        # seed self.find_node with the path tree root node
        return self.find_node(self.path_tree.root, tokens)

    def get_suggestions(self, tokens):
        # if nothing has been entered, suggest the valid descendent_methods
        # as per the root node
        if not tokens:
            rest_methods = self.path_tree.root.descendent_methods
            return rest_utils.rest_methods_to_crud(rest_methods)

        method = None
        if tokens[0] in CRUD_METHODS:
            method, tokens = tokens[0], tokens[1:]
            method = rest_utils.crud_to_rest(method)

        # final token might be either a full or a partial word.  Either way
        # we want to suggest completions
        suggestions = []

        # assume full word first
        nodes = self.find_node_from_root(tokens)
        if nodes:
            for node in nodes:
                suggestions.extend(
                    node.get_children_having_descendent_method(method))

                if method in node.methods and node.methods[method]:
                    params = ["{}=".format(m) for m in node.methods[method]]
                    suggestions.extend(params)

        # now assume partial word. If the first token was a valid CRUD method
        # then it will have been removed, and token list can be empty
        if not tokens:
            return suggestions

        # if we've got one token, there are two possibilities:
        #  - it's a partial entry of a valid method - autocomplete this
        #  - it's not a valid method - return the suggestions list as-is
        if not method and len(tokens) == 1:
            rest_methods = self.path_tree.root.descendent_methods
            crud_methods = rest_utils.rest_methods_to_crud(rest_methods)

            # is what we've already entered a partial match for a CRUD method?
            matching_crud_methods = [
                method for method in crud_methods
                if method.startswith(tokens[0])
            ]
            if not matching_crud_methods:
                return suggestions

            return crud_methods

        # assuming the last word we entered is a partial word, extract this
        # and perform autocomplete as above on original input minus this
        # last word
        partial, rest = tokens[-1], tokens[:-1]
        nodes = self.find_node_from_root(rest)
        if nodes:
            for node in nodes:
                # for each autocomplete suggestion, include it if our partial
                # word is a prefix of the suggestion.  Exclude it if our partial
                # matches the suggestion exactly
                partial_suggestions = [
                    name for name in
                    node.get_children_having_descendent_method(method)
                    if name.startswith(partial) and name != partial
                ]
                suggestions.extend(partial_suggestions)

                if method in node.methods and node.methods[method]:
                    partial_params = [
                        "{}=".format(m) for m in node.methods[method]
                        if m.startswith(partial) and m != partial
                    ]
                    suggestions.extend(partial_params)

        # remove duplicate by converting to set and back to list
        return list(set(suggestions))

if __name__ == "__main__":
    ac = autocomplete()
    print "{}\n\n".format(ac.path_tree)

    token_tests= [
        ["get", "books", "2"],
        ["get", "authors"],
        ["get", "authors", "1"],
        ["get", "authors", "1", "publications"],
        ["get", "authors", "1", "mismatch"],
    ]

    for test in token_tests:
        nodes = ac.find_node_from_root(test)
        suggestions = ac.get_suggestions(test)
        results = rest_utils.rest_call_from_tokens("localhost", "5123", test)

        print "For tokens {}, nodes are:".format(test)
        for node in nodes:
            print "Node is {}".format(node)

        print "Suggestions are {}".format(suggestions)
        print "Results are: "
        rest_utils.print_rest_api_response(results)

        print "\n\n"

    tokens = sys.argv[1:]
    nodes = ac.find_node_from_root(tokens)
    suggestions = ac.get_suggestions(tokens)
    results = rest_utils.rest_call_from_tokens("localhost", "5123", tokens)

    print "For tokens {}, nodes are:".format(tokens)
    for node in nodes:
        print "Node is {}".format(node)

    print "Suggestions are {}".format(suggestions)
    print "Results are: "
    rest_utils.print_rest_api_response(results)
