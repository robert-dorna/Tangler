from flask.testing import FlaskClient


def request(
    client: FlaskClient,
    method: str,
    path: str,
    *,
    json: dict | list | None = None,
    code=200
):
    response = getattr(client, method)(path, json=json)
    assert response.status_code == code

    response_json = response.json
    assert isinstance(response_json, dict)

    response_json_keys = list(response_json.keys())
    assert len(response_json_keys) == 2
    assert "result" in response_json_keys
    assert "result_summary" in response_json_keys

    if code == 200:
        assert response_json["result_summary"] == "request processed"
        return response_json["result"]

    return response_json


def get(client: FlaskClient, path: str, *, code=200):
    return request(client, "get", path, code=code)


def post(client: FlaskClient, path: str, *, json: dict | list, code=200):
    return request(client, "post", path, json=json, code=code)


def put(client: FlaskClient, path: str, *, json: dict | list, code=200):
    return request(client, "put", path, json=json, code=code)


def patch(client: FlaskClient, path: str, *, json: dict | list, code=200):
    return request(client, "patch", path, json=json, code=code)


def delete(
    client: FlaskClient, path: str, *, json: dict | list | None = None, code=200
):
    return request(client, "delete", path, json=json, code=code)
