from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

from src import config


class Game(BaseModel):
    poll_id: int
    chat_id: int
    results: dict  # Literal["Hitler Canceler", "Fascist Law", "Hitler Death", "Liberal Law"]
    creator_id: int

    @field_validator("results", mode="after")
    @classmethod
    def validate_results(cls, v: dict) -> Literal["CH", "DH", "FW", "LW"]:
        outcomes = set(v.values())
        if "I'm Canceler Hitler" in outcomes:
            return "CH"
        if "I'm Dead Hitler" in outcomes:
            return "DH"
        if (
            "I'm Liberal Winner"
            or "I'm Hitler Looser"
            or "I'm Fascistic Looser" in outcomes
        ):
            return "LW"
        if (
            "I'm Fascistic Winner"
            or "I'm Hitler Winner"
            or "I'm Liberal Looser" in outcomes
        ):
            return "FW"
        raise ValueError(
            f"Invalid results '{v}' for Game. Results must be one of {config.GAME_POLL_OUTCOMES}"
        )
