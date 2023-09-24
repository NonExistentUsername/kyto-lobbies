import time
from pathlib import Path

import pytest
import requests
from tenacity import retry, stop_after_delay

from engine import config


@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    return requests.get(config.get_api_url())


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "../engine/entrypoints/fastapi_app/app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
