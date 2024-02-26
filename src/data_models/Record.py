from typing import Literal, Optional

from pydantic import BaseModel, field_validator

from src import config


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

    def get_team(self) -> Optional[Literal["Fascist", "Liberal"]]:
        if (
            self.role == "CH"
            or self.role == "DH"
            or self.role == "FW"
            or self.role == "FL"
            or self.role == "HL"
        ):
            return "Fascist"
        elif self.role == "LW" or self.role == "LL":
            return "Liberal"
        else:
            return None
