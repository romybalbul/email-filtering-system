from fastapi.testclient import TestClient
from app.main import app


def test_filter_email_rejects_malicious_email(client, auth_headers):
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

    response = client.post(
        "/emails/filter",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "reject"


def test_filter_email_allows_trusted_sender(client, auth_headers):
    payload = {
        "sender": "employee@company.com",
        "recipient": "user@company.com",
        "subject": "Team update",
        "body": "Weekly sync notes",
        "attachments": []
    }

    response = client.post(
        "/emails/filter",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "allow"
