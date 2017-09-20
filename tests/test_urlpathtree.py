import os, pytest, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cli_plus.urlpathtree import urlpathtree
from cli_plus import swagger_utils

def get_swagger_file_path():
    swagger_filename = "swagger.json"
    return os.path.join(
        os.path.dirname(__file__),
        "data",
        swagger_filename)

@pytest.fixture(scope="session", autouse=True)
def get_swagger_definition():
    swagger_file_path = get_swagger_file_path()
    swagger_utils.get_swagger_api_definition(
        "localhost", "5123", swagger_file_path)

@pytest.mark.parametrize("method, children", [
    ("get", ["authors", "books"]),
    ("get", ["authors", "books"]),
    ("get", ["authors", "books"]),
    ("get", ["authors", "books"]),
])
def test_get_children_having_descendent_method(method, children):
    swagger_file_path = get_swagger_file_path()
    u = urlpathtree(swagger_file_path)
    u_children = u.root.get_children_having_descendent_method(method)

    assert len(children) == len(u_children)
    assert set(children) == set(u_children)
