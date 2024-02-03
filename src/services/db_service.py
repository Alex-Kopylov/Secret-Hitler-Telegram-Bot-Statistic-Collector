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
