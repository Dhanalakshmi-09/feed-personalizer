from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#Test: Valid Input
def test_valid_input():
    payload = {
        "user_id": "stu_4432",
        "user_profile": {
            "branches_of_interest": ["CSE"],
            "tags_followed": ["python"],
            "buddies": ["stu_123"],
            "active_hours": ["08:00-11:00"]
        },
        "posts": [
            {
                "post_id": "post1",
                "author_id": "stu_123",
                "tags": ["python"],
                "content_type": "text",
                "karma": 50,
                "created_at": "2024-07-18T09:45:00Z"
            }
        ]
    }
    res = client.post("/rank-feed", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ranked"
    assert len(body["ranked_posts"]) == 1
    assert "score" in body["ranked_posts"][0]

#Test: Empty Post List
def test_empty_post_list():
    payload = {
        "user_id": "stu_4432",
        "user_profile": {
            "branches_of_interest": ["CSE"],
            "tags_followed": ["python"],
            "buddies": [],
            "active_hours": ["08:00-11:00"]
        },
        "posts": []
    }
    res = client.post("/rank-feed", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert body["ranked_posts"] == []

#Test: Invalid content_type (should fail schema validation)
def test_invalid_content_type():
    payload = {
        "user_id": "stu_4432",
        "user_profile": {
            "branches_of_interest": ["CSE"],
            "tags_followed": ["python"],
            "buddies": [],
            "active_hours": ["08:00-11:00"]
        },
        "posts": [
            {
                "post_id": "post1",
                "author_id": "stu_123",
                "tags": ["python"],
                "content_type": "pdf",  # Invalid
                "karma": 50,
                "created_at": "2024-07-18T09:45:00Z"
            }
        ]
    }
    res = client.post("/rank-feed", json=payload)
    assert res.status_code == 422  # Validation error

#Test: Missing required field (karma)
def test_missing_required_field():
    payload = {
        "user_id": "stu_4432",
        "user_profile": {
            "branches_of_interest": ["CSE"],
            "tags_followed": ["python"],
            "buddies": [],
            "active_hours": ["08:00-11:00"]
        },
        "posts": [
            {
                "post_id": "post1",
                "author_id": "stu_123",
                "tags": ["python"],
                "content_type": "text",
                # 'karma' is missing
                "created_at": "2024-07-18T09:45:00Z"
            }
        ]
    }
    res = client.post("/rank-feed", json=payload)
    assert res.status_code == 422

#Test: Invalid date format
def test_invalid_date_format():
    payload = {
        "user_id": "stu_4432",
        "user_profile": {
            "branches_of_interest": ["CSE"],
            "tags_followed": ["python"],
            "buddies": [],
            "active_hours": ["08:00-11:00"]
        },
        "posts": [
            {
                "post_id": "post1",
                "author_id": "stu_123",
                "tags": ["python"],
                "content_type": "text",
                "karma": 50,
                "created_at": "not-a-valid-date"
            }
        ]
    }
    res = client.post("/rank-feed", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert len(body["ranked_posts"]) == 1
    assert "score" in body["ranked_posts"][0]
