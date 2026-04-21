from fastapi.testclient import TestClient
from app.main import app


def test_filter_email_rejects_malicious_email():
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
        response = client.post("/emails/filter", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["verdict"] == "reject"
    assert data["score"] >= 120
    assert len(data["reasons"]) >= 1
    assert len(data["matched_rules"]) >= 1


def test_filter_email_allows_trusted_sender():
    payload = {
        "sender": "employee@company.com",
        "recipient": "user@company.com",
        "subject": "Team update",
        "body": "Weekly sync notes",
        "attachments": []
    }

    with TestClient(app) as client:
        response = client.post("/emails/filter", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["verdict"] == "allow"
