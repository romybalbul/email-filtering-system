from fastapi.testclient import TestClient

from app.main import app


def test_list_entries_can_be_added_and_removed():
    with TestClient(app) as client:
        list_response = client.get("/lists/blocked_senders")
        assert list_response.status_code == 200

        post_response = client.post(
            "/lists/blocked_senders",
            json={"value": "newbad@evil.com"},
        )
        assert post_response.status_code == 200
        created = post_response.json()
        assert created["list_type"] == "blocked_senders"
        assert created["value"] == "newbad@evil.com"

        list_after_response = client.get("/lists/blocked_senders")
        assert list_after_response.status_code == 200
        values = [item["value"] for item in list_after_response.json()]
        assert "newbad@evil.com" in values

        delete_response = client.delete(f"/lists/blocked_senders/{created['id']}")
        assert delete_response.status_code == 204


def test_filtering_uses_db_backed_blocked_senders():
    with TestClient(app) as client:
        client.post("/lists/blocked_senders", json={"value": "db-added@evil.com"})

        payload = {
            "sender": "db-added@evil.com",
            "recipient": "user@company.com",
            "subject": "hello",
            "body": "normal body",
            "attachments": []
        }

        response = client.post("/emails/filter", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["verdict"] in {"reject", "quarantine", "spam"}
        assert any(rule["rule"] == "blacklist_rule" for rule in data["matched_rules"])
