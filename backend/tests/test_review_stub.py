from fastapi.testclient import TestClient

from app.main import app


def test_review_endpoint_returns_stub_without_api_key():
    client = TestClient(app)
    payload = {
        "repo_full_name": "owner/repo",
        "pr_number": 1,
        "title": "Test PR",
        "body": "Ensure stub review works",
        "files": [
            {
                "filename": "example.py",
                "patch": "diff --git a/example.py b/example.py\n+print('hello')\n",
            }
        ],
    }

    response = client.post("/review", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["score"], int)
    assert "warnings" in data
    assert data["findings"], "Expected at least one fallback finding"
