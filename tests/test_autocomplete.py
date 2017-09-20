import os, pytest, sys

sys.path.append("..")

from cli_plus.autocomplete import autocomplete

@pytest.mark.parametrize("tokens, suggestions", [
    (["get"], ["authors", "books"]),
    (["get", "books", "2"], []),
    (["get", "authors"], ["[id]"]),
    (["get", "authors", "1"], []),
    (["get", "authors", "1", "publications"], []),
    (["get", "authors", "1", "mismatch"], [])
])
def test_suggestions(tokens, suggestions):
    swagger_filename = "swagger.json"
    file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        swagger_filename)
    ac = autocomplete(file_path)
    ac_suggestions = ac.get_suggestions(tokens)

    assert len(suggestions) == len(ac_suggestions)
    assert set(suggestions) == set(ac_suggestions)
