from typing import Literal, Optional

from pydantic import BaseModel, Field


class Poll(BaseModel):
    id: int
    message_id: int
    chat_id: int
    chat_name: str
    creator_id: int
    creator_username: Optional[str | None] = Field(None)
