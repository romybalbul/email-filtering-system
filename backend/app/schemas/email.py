from pydantic import BaseModel, Field
from typing import List


class AttachmentInput(BaseModel):
    filename: str
    content_type: str | None = None
    size: int | None = None


class EmailInput(BaseModel):
    sender: str
    recipient: str
    subject: str = ""
    body: str = ""
    attachments: List[AttachmentInput] = Field(default_factory=list)
