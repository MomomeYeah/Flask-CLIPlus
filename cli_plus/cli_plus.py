import os, sys

from autocomplete import autocomplete
from swagger_utils import get_swagger_api_definition

if __name__ == "__main__":

    # store swagger definition at ~/cli_plus/swagger.json
    swagger_filename = "swagger.json"
    api_definition_location = os.path.expanduser("~/.cli_plus")
    swagger_file_path = "{}/{}".format(api_definition_location, swagger_filename)

    # ensure ~/.cli_plus directory exists
    if not os.path.exists(api_definition_location):
        os.makedirs(api_definition_location)

    # get API definition
    get_swagger_api_definition("localhost", "5123", swagger_file_path)

    # create autocomplete object
    ac = autocomplete(swagger_file_path)

    # first two args will be:
    #   - the full path to __file__
    #   - the program we're calling
    # actual autocomplete tokens come after this
    for suggestion in ac.get_suggestions(sys.argv[2:]):
        print suggestion
