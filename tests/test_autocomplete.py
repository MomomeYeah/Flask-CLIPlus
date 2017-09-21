import os, pytest, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cli_plus.autocomplete import autocomplete

def get_swagger_file_path():
    swagger_filename = "swagger.json"
    return os.path.join(
        os.path.dirname(__file__),
        "data",
        swagger_filename)

@pytest.mark.parametrize("tokens, suggestions", [
    (["get"], ["authors", "books"]),
    (["get", "books", "2"], []),
    (["get", "authors"], ["[id]"]),
    (["get", "authors", "1"], []),
    (["get", "authors", "1", "publications"], []),
    (["get", "authors", "1", "mismatch"], [])
])
def test_suggestions(tokens, suggestions):
    swagger_file_path = get_swagger_file_path()
    ac = autocomplete(swagger_file_path)
    ac_suggestions = ac.get_suggestions(tokens)

    assert len(suggestions) == len(ac_suggestions)
    assert set(suggestions) == set(ac_suggestions)
