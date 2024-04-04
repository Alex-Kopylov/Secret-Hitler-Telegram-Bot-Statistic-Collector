from typing import Optional
from pydantic import BaseModel, field_validator, Field
import re


class Player(BaseModel):
    telegram_user_id: int
    username: Optional[str | None] = Field(None)
    first_name: Optional[str | None]
    full_name: Optional[str | None]
    last_name: Optional[str | None]
    is_bot: Optional[bool] = False
    language_code: Optional[str | None]

    @field_validator("is_bot", mode="after")
    @classmethod
    def validate_bot(cls, v: bool) -> str:
        return (
            "TRUE" if v else "FALSE"
        )  # sqlite3 does not support a boolean type # todo maybe use 1 and 0

    @field_validator("username", mode="after")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return re.sub(r"[\W_]+", "", v)
