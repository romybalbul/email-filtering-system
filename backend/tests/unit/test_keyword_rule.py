from app.schemas.email import EmailInput
from app.services.rules.keyword_rule import KeywordRule


def test_keyword_rule_matches_suspicious_word():
    rule = KeywordRule(keywords={"urgent"}, score=30)

    email = EmailInput(
        sender="a@test.com",
        recipient="b@test.com",
        subject="Urgent action required",
        body="hello",
        attachments=[],
    )

    result = rule.evaluate(email)

    assert result.matched is True
    assert result.score_delta == 30
    assert "urgent" in result.reason.lower()
