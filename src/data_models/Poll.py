from typing import Literal

from pydantic import BaseModel


class Poll(BaseModel):
    id: int
    message_id: int
    chat_id: int
    chat_name: str
    creator_id: int
    creator_username: str
