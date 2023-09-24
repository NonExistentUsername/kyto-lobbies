from typing import Dict

import requests

from engine import config


def post_create_player(username: str) -> Dict:
    return requests.post(
        f"{config.get_api_url()}/players",
        json={"username": username},
    ).json()


def post_create_room(creator_id: str) -> Dict:
    return requests.post(
        f"{config.get_api_url()}/rooms",
        json={"creator_id": creator_id},
    ).json()
