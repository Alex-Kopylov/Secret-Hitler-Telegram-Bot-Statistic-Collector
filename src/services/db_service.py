import logging
import sqlite3

from src.data_models.Playroom import Playroom
from src.data_models.Record import Record
from src.db import execute


async def save_record(record: Record) -> None:
    await execute(
        """INSERT INTO records (creator_id, player_id, playroom_id, game_id, role)
        VALUES (?, ?, ?, ?, ?)""",
        (
            record.creator_id,
            record.player_id,
            record.playroom_id,
            record.game_id,
            record.role,
        ),
    )


async def save_playroom(playroom: Playroom) -> None:
    """Add a game room to the bot_data"""
    try:
        await execute(
            "INSERT INTO playrooms (id, name) VALUES (?, ?)",
            (playroom.telegram_chat_id, playroom.name),
        )
    except sqlite3.IntegrityError:
        logging.info(f"Playroom {playroom.name} already exists in the database")
