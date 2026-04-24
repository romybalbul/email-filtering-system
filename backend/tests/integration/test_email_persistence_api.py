def test_filter_email_persists_and_can_be_fetched(client, auth_headers):
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

    post_response = client.post(
        "/emails/filter",
        json=payload,
        headers=auth_headers,
    )
    assert post_response.status_code == 200

    email_id = post_response.json()["email_id"]

    get_response = client.get(
        f"/emails/{email_id}",
        headers=auth_headers,
    )
    assert get_response.status_code == 200
