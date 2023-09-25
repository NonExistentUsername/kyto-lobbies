from typing import Dict

from fastapi.testclient import TestClient

from engine import config
from engine.entrypoints.fastapi_app.app import create_app

_client = TestClient(create_app())


def post_create_player(username: str) -> Dict:
    return _client.post(
        f"{config.get_api_url()}/v1/players",
        params={"username": username},
    ).json()


def get_room(room_id: str) -> Dict:
    return _client.get(
        f"{config.get_api_url()}/v1/rooms/{room_id}",
    ).json()


def post_create_room(creator_id: str) -> Dict:
    return _client.post(
        f"{config.get_api_url()}/v1/rooms",
        params={"creator_id": creator_id},
    ).json()


def join_room(room_id: str, player_id: str) -> Dict:
    return _client.post(
        f"{config.get_api_url()}/v1/rooms/{room_id}/join",
        params={"player_id": player_id},
    ).json()


def leave_room(room_id: str, player_id: str) -> Dict:
    return _client.post(
        f"{config.get_api_url()}/v1/rooms/{room_id}/leave",
        params={"player_id": player_id},
    ).json()
