from . import api_client


def assert_default_format(response):
    assert "status_code" in response
    assert "success" in response
    assert "message" in response
    assert "data" in response

    assert isinstance(response["status_code"], int)
    assert isinstance(response["success"], bool)
    assert isinstance(response["message"], str)
    assert isinstance(response["data"], dict)


def test_create_player():
    response = api_client.post_create_player(username="testuser")

    assert_default_format(response)
    data = response["data"]

    assert "id" in data
    assert "username" in data
    assert data["username"] == "testuser"
