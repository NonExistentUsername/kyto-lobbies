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


def test_join_room():
    response = api_client.post_create_player(username="testuser3")

    assert_default_format(response)
    creator_id = response["data"]["id"]

    response = api_client.post_create_player(username="testuser4")

    assert_default_format(response)
    first_player_id = response["data"]["id"]

    response = api_client.post_create_player(username="testuser5")

    assert_default_format(response)
    second_player_id = response["data"]["id"]

    response = api_client.post_create_room(creator_id=creator_id)

    assert_default_format(response)
    room_id = response["data"]["id"]

    response = api_client.join_room(room_id=room_id, player_id=first_player_id)

    assert_default_format(response)
    assert response["status_code"] == 200
    assert response["success"] is True

    response = api_client.join_room(room_id=room_id, player_id=second_player_id)

    assert_default_format(response)
    assert response["status_code"] == 200
    assert response["success"] is True

    response = api_client.join_room(room_id=room_id, player_id=second_player_id)

    assert_default_format(response)
    assert response["status_code"] == 409
    assert response["success"] is False

    response = api_client.join_room(room_id="invalid", player_id=second_player_id)

    assert_default_format(response)
    assert response["status_code"] == 404
    assert response["success"] is False

    response = api_client.join_room(room_id=room_id, player_id="invalid")

    assert_default_format(response)
    assert response["status_code"] == 404
