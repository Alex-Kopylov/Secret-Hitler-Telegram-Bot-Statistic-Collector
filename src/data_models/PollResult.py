from pydantic import BaseModel, Field

from src.config import AppConfig


class PollResult(BaseModel):
    poll_id: int
    user_id: int
    answer: int = Field(ge=0, le=len(AppConfig().game_poll_outcomes))

    def get_answer_as_text(self) -> str:
        return AppConfig().game_poll_outcomes[self.answer]
