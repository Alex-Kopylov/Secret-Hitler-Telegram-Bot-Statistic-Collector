from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Game(BaseModel):
    playroom_id: int
    end_time: datetime
    result: Literal["Hitler Canceler", "Fascist Law", "Hitler Death", "Liberal Law"]
