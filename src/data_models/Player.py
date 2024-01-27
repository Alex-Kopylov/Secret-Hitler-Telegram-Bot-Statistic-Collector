from typing import Optional

from pydantic import BaseModel


class Player(BaseModel):
    telegram_user_id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_bot: bool = False
