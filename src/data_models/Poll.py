from datetime import datetime

from pydantic import BaseModel
from typing import Literal


class Poll(BaseModel):
    poll_id: int
    message_id: int
    chat_id: int
    creator_id: int
    poll_type: Literal["default_game"] = "default"
