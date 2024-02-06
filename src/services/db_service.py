import logging
import sqlite3

from src.data_models.Playroom import Playroom
import logging
import sqlite3

from src.data_models.Game import Game
from src.data_models.Player import Player
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


async def save_playroom(playroom: Playroom) -> None:
    """Add a game room to the bot_data"""
    try:
        await execute(
            "INSERT INTO playrooms (id, name) VALUES (?, ?)",
            (playroom.telegram_chat_id, playroom.name),
        )
    except sqlite3.IntegrityError:
        logging.info(f"Playroom {playroom.name} already exists in the database")


async def save_player(player: Player) -> None:
    """Add a player to the bot_data"""
    try:
        await execute(
            "INSERT INTO players (id, username, first_name, full_name, last_name, is_bot, language_code) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                player.telegram_user_id,
                player.username,
                player.first_name,
                player.full_name,
                player.last_name,
                player.is_bot,
                player.language_code,
            ),
        )
    except sqlite3.IntegrityError:
        logging.info(f"Player {player.username} already exists in the database")


async def save_game(game: Game) -> None:
    """Add a game to the bot_data"""
    try:
        await execute(
            "INSERT INTO games (id, playroom_id, creator_id, result) VALUES (?, ?, ?, ?)",
            (game.poll_id, game.chat_id, game.creator_id, game.results),
        )
    except sqlite3.IntegrityError:
        logging.info(f"Game {game.poll_id} already exists in the database")
