def test_list_entries_can_be_added_and_removed(client, auth_headers):
    list_response = client.get("/lists/blocked_senders", headers=auth_headers)
    assert list_response.status_code == 200

    post_response = client.post(
        "/lists/blocked_senders",
        json={"value": "newbad@evil.com"},
        headers=auth_headers,
    )
    assert post_response.status_code == 200

    created = post_response.json()

    delete_response = client.delete(
        f"/lists/blocked_senders/{created['id']}",
        headers=auth_headers,
    )
    assert delete_response.status_code == 204


def test_filtering_uses_db_backed_blocked_senders(client, auth_headers):
    client.post(
        "/lists/blocked_senders",
        json={"value": "db-added@evil.com"},
        headers=auth_headers,
    )

    payload = {
        "sender": "db-added@evil.com",
        "recipient": "user@company.com",
        "subject": "hello",
        "body": "normal body",
        "attachments": []
    }

    response = client.post(
        "/emails/filter",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert any(rule["rule"] == "blacklist_rule" for rule in data["matched_rules"])
