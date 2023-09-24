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
    response = api_client.post_create_player(username="")
    assert_default_format(response)

    assert response["status_code"] == 400
    assert response["success"] is False

    response = api_client.post_create_player(username="testuser")

    assert_default_format(response)
    data = response["data"]

    assert "id" in data
    assert "username" in data
    assert data["username"] == "testuser"
    assert response["status_code"] == 201
    assert response["success"] is True

    response = api_client.post_create_player(username="testuser")
    assert_default_format(response)

    assert response["status_code"] == 409
    assert response["success"] is False


def test_create_room():
    response = api_client.post_create_player(username="testuser2")

    assert_default_format(response)
    player_id = response["data"]["id"]

    response = api_client.post_create_room(creator_id="")
    assert_default_format(response)

    assert response["status_code"] == 404
    assert response["success"] is False

    response = api_client.post_create_room(creator_id=player_id)

    assert_default_format(response)
    data = response["data"]

    assert "id" in data
    assert "creator_id" in data
    assert response["status_code"] == 201
    assert response["success"] is True

    response = api_client.post_create_room(creator_id=player_id)

    assert_default_format(response)
    assert response["status_code"] == 409
    assert response["success"] is False
