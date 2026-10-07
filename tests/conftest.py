from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


_INITIAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture
def activities(monkeypatch):
    activities = deepcopy(_INITIAL_ACTIVITIES)
    monkeypatch.setattr(app_module, "activities", activities)
    return activities


@pytest.fixture
def client(activities):
    with TestClient(app_module.app) as test_client:
        yield test_client
