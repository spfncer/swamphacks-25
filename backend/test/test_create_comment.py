import pytest

@pytest.mark.asyncio
async def test_create_comment(client):
    test_comment = {
        "body": "This is a test comment.",
        "author": "TestUser",
        "webpage": "example.com"
    }

    response = client.post("/comments/", json=test_comment)

    assert response.status_code == 201

    data = response.json()
    assert data["body"] == "This is a test comment."
    assert data["author"] == "TestUser"
    assert data["webpage"] == "example.com"
