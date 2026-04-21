from app.services.rules.base import BaseRule, RuleResult


class AttachmentRule(BaseRule):
    name = "attachment_rule"

    def __init__(self, blocked_extensions: set[str], score: int = 80):
        self.blocked_extensions = {ext.lower() for ext in blocked_extensions}
        self.score = score

    def evaluate(self, email) -> RuleResult:
        for attachment in email.attachments:
            filename = attachment.filename.lower()
            for ext in self.blocked_extensions:
                if filename.endswith(ext):
                    return RuleResult(
                        matched=True,
                        score_delta=self.score,
                        reason=f"blocked attachment extension detected: {ext}",
                    )

        return RuleResult(matched=False)
