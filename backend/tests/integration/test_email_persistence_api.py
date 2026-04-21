from fastapi.testclient import TestClient
from app.main import app


def test_filter_email_persists_and_can_be_fetched():
    payload = {
        "sender": "attacker@evil-example.com",
        "recipient": "user@company.com",
        "subject": "URGENT invoice attached",
        "body": "Please verify your password immediately",
        "attachments": [
            {
                "filename": "invoice.exe",
                "content_type": "application/octet-stream",
                "size": 12345
            }
        ]
    }

    with TestClient(app) as client:
        post_response = client.post("/emails/filter", json=payload)
        assert post_response.status_code == 200

        data = post_response.json()
        assert data["email_id"] is not None
        email_id = data["email_id"]

        get_response = client.get(f"/emails/{email_id}")
        assert get_response.status_code == 200

    stored = get_response.json()
    assert stored["id"] == email_id
    assert stored["sender"] == payload["sender"]
    assert stored["recipient"] == payload["recipient"]
    assert stored["verdict"] == "reject"
