from fastapi.testclient import TestClient
from app.main import app


def test_filter_email_saves_rule_hits_and_returns_them():
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

        email_id = post_response.json()["email_id"]
        assert email_id is not None

        detail_response = client.get(f"/emails/{email_id}")
        assert detail_response.status_code == 200

        detail_data = detail_response.json()
        assert len(detail_data["rule_hits"]) >= 1

        rule_hits_response = client.get(f"/emails/{email_id}/rule-hits")
        assert rule_hits_response.status_code == 200

        hits = rule_hits_response.json()
        assert len(hits) >= 1
        assert all(hit["email_id"] == email_id for hit in hits)
        assert any(hit["rule_name"] == "blacklist_rule" for hit in hits)
