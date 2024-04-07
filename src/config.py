from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Tuple
from pathlib import Path

from telegram import BotCommand


class AppConfig(BaseSettings):
    # Define each configuration item with type annotations
    telegram_bot_token: str | None = Field(default=None, env="TELEGRAM_BOT_TOKEN")
    developer_chat_id: str | None = Field(default=None, env="DEVELOPER_CHAT_ID")
    sqlite_db_file_path: Path | str = Field(
        default=Path().resolve() / "db.sqlite", env="SQLITE_DB_FILE_PATH"
    )
    date_format: str = "%d.%m.%Y %H:%M:%S"

    # Game constants
    max_votes: int = 10
    max_hitler_voters: int = 1
    min_hitler_voters: int = 1
    max_liberal_voters: int = 6
    min_liberal_voters: int = 3
    max_fascist_voters: int = 3
    min_fascist_voters: int = 1

    # Game poll outcomes
    game_poll_outcomes: Tuple[str, ...] = (
        "👀 SPECTATOR | NOT A PLAYER 👀",
        "I'm Chancellor Hitler",
        "I'm Dead Hitler",
        "I'm Hitler Loser",
        "I'm Hitler Winner",
        "I'm Liberal Winner",
        "I'm Liberal Loser",
        "I'm Fascistic Winner",
        "I'm Fascistic Loser",
    )

    # Colors
    liberal_color: str = "#61C8D9"
    liberal_color_stroke: str = "#38586D"
    fascist_color: str = "#E66443"
    fascist_color_stroke: str = "#7A1E16"
    stroke_size: str = "12"  # TODO: pydantic int setter, str getter

    commands: list[BotCommand] = Field(
        [
            BotCommand("start", "Start using bot"),
            BotCommand("help", "Display help"),
            BotCommand("game", "Start the game in group chat"),
            BotCommand("save", "Save the game by replying to poll created by /game command"),
            BotCommand("mystats", "Visualise your personal statistics"),
        ]
    )

    class Config:
        # Optional: control the source of environment variables
        env_file = ".env"
        env_file_encoding = "utf-8"
