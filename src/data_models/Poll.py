from typing import Literal

from pydantic import BaseModel


class Poll(BaseModel):
    poll_id: int
    message_id: int
    chat_id: int
    creator_id: int
    poll_type: Literal["default_game"] = "default"
