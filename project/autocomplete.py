#!/usr/bin/python

import os, sys

from rest_utils import CRUD_METHODS, REST_METHODS
from rest_utils import print_rest_api_response, rest_call_from_tokens
from rest_utils import crud_to_rest, rest_methods_to_crud
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

    # TODO: handle scenario where first token isn't a CRUD
    #
    # TODO: entering a wildcard with a value like {id} doesn't seem to work?
    #
    # TODO: POST/PUT params: key=value format
    # TODO: params: quotes to allow spaces, or not?
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
            return rest_methods_to_crud(rest_methods)

        method = None
        if tokens[0] in CRUD_METHODS:
            method, tokens = tokens[0], tokens[1:]
            method = crud_to_rest(method)

        # final token might be either a full or a partial word.  Either way
        # we want to suggest completions
        suggestions = []

        # assume full word first
        nodes = self.find_node_from_root(tokens)
        if nodes:
            for node in nodes:
                suggestions.extend(
                    node.get_children_having_descendent_method(method))

        # assume partial word
        if len(tokens) == 0:
            return suggestions

        if not method and len(tokens) == 1:
            rest_methods = self.path_tree.root.descendent_methods
            return rest_methods_to_crud(rest_methods)

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
                    if name.startswith(partial) and name != partial]

                suggestions.extend(partial_suggestions)

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
        results = rest_call_from_tokens("localhost", "5123", test)

        print "For tokens {}, nodes are:".format(test)
        for node in nodes:
            print "Node is {}".format(node)

        print "Suggestions are {}".format(suggestions)
        print "Results are: "
        print_rest_api_response(results)

        print "\n\n"

    tokens = sys.argv[1:]
    nodes = ac.find_node_from_root(tokens)
    suggestions = ac.get_suggestions(tokens)
    results = rest_call_from_tokens("localhost", "5123", tokens)

    print "For tokens {}, nodes are:".format(tokens)
    for node in nodes:
        print "Node is {}".format(node)

    print "Suggestions are {}".format(suggestions)
    print "Results are: "
    print_rest_api_response(results)
