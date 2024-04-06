from typing import Literal, Tuple

from pydantic import BaseModel, field_validator
from collections import Counter
from src.data_models.PollResult import PollResult


class Game(BaseModel):
    poll_id: int
    chat_id: int
    results: tuple[
        PollResult, ...
    ]  # Literal["Hitler Chancellor", "Fascist Law", "Hitler Death", "Liberal Law"]
    creator_id: int

    def extract_player_outcomes(cls, results: Tuple[PollResult, ...]) -> Counter:
        outcomes = [outcome.get_answer_as_text() for outcome in results]
        return Counter(outcomes)

    def remove_spectators(cls, outcomes_counter: Counter) -> None:
        outcomes_counter.pop("👀 SPECTATOR | NOT A PLAYER 👀", None)

    def count_player_roles(cls, outcomes_counter: Counter) -> tuple[int, int, int]:
        total_hitlers = sum(
            outcomes_counter[role]
            for role in [
                "I'm Chancellor Hitler",
                "I'm Dead Hitler",
                "I'm Hitler Loser",
                "I'm Hitler Winner",
            ]
        )
        total_liberals = (
            outcomes_counter["I'm Liberal Winner"]
            + outcomes_counter["I'm Liberal Loser"]
        )
        total_fascists = (
            outcomes_counter["I'm Fascistic Winner"]
            + outcomes_counter["I'm Fascistic Loser"]
            + total_hitlers
        )
        return total_hitlers, total_liberals, total_fascists

    def validate_player_distribution(
        cls,
        total_hitlers: int,
        total_liberals: int,
        total_fascists: int,
        max_hitlers: int = 1,
        max_liberals: int = 6,
        max_fascists: int = 4,
    ) -> None:
        if (
            total_hitlers > max_hitlers
            or total_liberals > max_liberals
            or total_fascists > max_fascists
        ):
            raise ValueError("Invalid player distribution according to game rules.")

    def check_mutually_exclusive_victory_conditions(
        cls, outcomes_counter: Counter
    ) -> None:
        liberal_win = (
            outcomes_counter["I'm Liberal Winner"] > 0
            or outcomes_counter["I'm Dead Hitler"] > 0
            or outcomes_counter["I'm Fascistic Loser"] > 0
            or outcomes_counter["I'm Hitler Loser"] > 0
        )

        fascist_win = (
            outcomes_counter["I'm Fascistic Winner"] > 0
            or outcomes_counter["I'm Hitler Winner"] > 0
            or outcomes_counter["I'm Chancellor Hitler"] > 0
            or outcomes_counter["I'm Liberal Loser"] > 0
        )
        if liberal_win and fascist_win:
            raise ValueError("Invalid results: Winners from both teams cannot exist.")

    @field_validator("results", mode="after")
    def validate_results(
        cls, results: tuple[PollResult]
    ) -> Literal["CH", "DH", "FW", "LW"]:
        outcomes_counter = cls.extract_player_outcomes(results)
        cls.remove_spectators(outcomes_counter)
        total_hitlers, total_liberals, total_fascists = cls.count_player_roles(
            outcomes_counter
        )
        cls.validate_player_distribution(total_hitlers, total_liberals, total_fascists)
        cls.check_mutually_exclusive_victory_conditions(outcomes_counter)

        # Determine outcome based on specific conditions
        if outcomes_counter["I'm Chancellor Hitler"] > 0:
            return "CH"
        if outcomes_counter["I'm Dead Hitler"] > 0:
            return "DH"
        if outcomes_counter["I'm Liberal Winner"] > 0:
            return "LW"
        if (
            outcomes_counter["I'm Fascistic Winner"] > 0
            or outcomes_counter["I'm Hitler Winner"] > 0
        ):
            return "FW"

        raise ValueError("Invalid game results: No clear win condition met.")
