from enum import Enum
from typing import Literal, Optional
from src import config
from pydantic import BaseModel, field_validator


class Record(BaseModel):
    creator_id: int
    player_id: int
    playroom_id: int
    game_id: int
    role: str

    @field_validator("role", mode="after")
    @classmethod
    def shorten_role(
        cls, v: str
    ) -> Optional[Literal["CH", "DH", "HW", "HL", "LW", "LL", "FW", "FL"] | None]:
        match v:
            case "I'm Canceler Hitler":
                return "CH"
            case "I'm Dead Hitler":
                return "DH"
            case "I'm Hitler Winner":
                return "HW"
            case "I'm Liberal Winner":
                return "LW"
            case "I'm Hitler Loser":
                return "HL"
            case "I'm Liberal Loser":
                return "LL"
            case "I'm Fascistic Winner":
                return "FW"
            case "I'm Fascistic Loser":
                return "FL"
            case "👀 SPECTATOR | NOT A PLAYER 👀":
                return None
            case _:
                raise ValueError(
                    f"Invalid role '{v}' for Record. Role must be one of {config.GAME_POLL_OUTCOMES}"
                )
