#!/usr/bin/python

import os, sys

sys.path.append("..")

from cli_plus import rest_utils

if __name__ == "__main__":
    tokens = sys.argv[1:]
    results = rest_utils.rest_call_from_tokens("localhost", "5123", tokens)

    print "Results are: "
    rest_utils.print_rest_api_response(results)
