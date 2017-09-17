import sys

from autocomplete import autocomplete

if __name__ == "__main__":
    ac = autocomplete()

    # first two args will be:
    #   - the full path to __file__
    #   - the program we're calling
    # actual autocomplete tokens come after this
    for suggestion in ac.get_suggestions(sys.argv[2:]):
        print suggestion
