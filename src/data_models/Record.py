from typing import Literal

from pydantic import BaseModel, field_validator


class Record(BaseModel):
    player_id: int
    game_id: int
    role: Literal["Hitler", "Fascist", "Liberal"]
    won: bool

    @field_validator("won", mode="after")
    @classmethod
    def convert_bool_to_int(cls, v: bool) -> int:
        return int(v)

    @field_validator("role", mode="after")
    @classmethod
    def shorten_role(cls, v: str) -> str:
        return v[0]
