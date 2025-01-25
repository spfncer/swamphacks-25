import pytest
from mongomock_motor import AsyncMongoMockClient
from fastapi.testclient import TestClient

from app import main

def get_test_db():
    return AsyncMongoMockClient()

@pytest.fixture
def client():
    # Create app with mocked database
    main.app.dependency_overrides["get_prod_db"] = get_test_db
    return TestClient(main.app)
