from pydantic import BaseModel


class Playroom(BaseModel):
    telegram_chat_id: int
    name: str
