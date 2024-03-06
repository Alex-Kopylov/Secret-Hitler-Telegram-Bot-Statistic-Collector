import logging
import sqlite3

from src.data_models.Game import Game
from src.data_models.Player import Player
from src.data_models.Playroom import Playroom
from src.data_models.Poll import Poll
from src.data_models.PollResult import PollResult
from src.data_models.Record import Record
from src.db import execute, fetch_one, fetch_all


async def save_record(record: Record) -> None:
    try:
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
    except sqlite3.IntegrityError:
        logging.info(
            f"Something went wrong with game: {record.game_id} in playroom {record.playroom_id}"
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


async def save_poll(poll: Poll) -> None:
    """Add a poll to the database"""
    try:
        await execute(
            """INSERT INTO polls (id, message_id, chat_id, chat_name, creator_id, creator_username)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                poll.id,
                poll.message_id,
                poll.chat_id,
                poll.chat_name,
                poll.creator_id,
                poll.creator_username,
            ),
        )
    except sqlite3.IntegrityError:
        logging.info(
            f"Poll with message_id {poll.message_id} already exists in the database"
        )


async def save_poll_result(poll_result: PollResult) -> None:
    """Add a poll result to the database"""
    try:
        await execute(
            """INSERT INTO poll_results (poll_id, user_id, answer)
            VALUES (?, ?, ?)
            ON CONFLICT(poll_id, user_id)
            DO UPDATE SET answer=excluded.answer""",
            (
                poll_result.poll_id,
                poll_result.user_id,
                poll_result.answer,
            ),
        )
    except sqlite3.IntegrityError:
        logging.info(
            f"Could not save or update poll result for poll ID {poll_result.poll_id}"
        )


async def delete_poll_result(poll_id: int, user_id: int) -> None:
    """Delete a poll result from the database"""
    try:
        await execute(
            "DELETE FROM poll_results WHERE poll_id = ? AND user_id = ?",
            (poll_id, user_id),
        )
    except Exception as e:
        logging.error(
            f"Error deleting poll result for poll_id {poll_id} and user_id {user_id}: {e}"
        )


async def fetch_poll_data(poll_id: int) -> Poll | None:
    sql = """SELECT id, message_id, chat_id, chat_name, creator_id, creator_username
             FROM polls
             WHERE id = ?"""
    result = await fetch_one(sql, [poll_id])
    if result:
        return Poll(**result)
    return None


async def fetch_poll_results(poll_id: int) -> tuple[PollResult]:
    sql = """SELECT poll_id, user_id, answer
             FROM poll_results
             WHERE poll_id = ?"""
    results = await fetch_all(sql, [poll_id])
    return tuple(PollResult(**result) for result in results)


async def fetch_player_answers(username):
    """
    Returns table of player with given username results grouped by his answers
    
    Parameters:
    -----------
    cur : sqlite3 cursor
        Cursor to the given database.
        
    username : string from table Players.username
        Username of given player.
    
    Returns:
    --------
    res : dict
        Keys are answers, values are count numbers
    """
    query = f"""SELECT SUM(CASE WHEN records.role = 'HC' THEN 1 ELSE 0 END) AS HC, 
                       SUM(CASE WHEN records.role = 'HD' THEN 1 ELSE 0 END) AS HD, 
                       SUM(CASE WHEN records.role = 'HL' THEN 1 ELSE 0 END) AS HL, 
                       SUM(CASE WHEN records.role = 'HW' THEN 1 ELSE 0 END) AS HW, 
                       SUM(CASE WHEN records.role = 'FL' THEN 1 ELSE 0 END) AS FL, 
                       SUM(CASE WHEN records.role = 'LL' THEN 1 ELSE 0 END) AS LL, 
                       SUM(CASE WHEN records.role = 'LW' THEN 1 ELSE 0 END) AS LW, 
                       SUM(CASE WHEN records.role = 'FW' THEN 1 ELSE 0 END) AS FW
                FROM Records 
                INNER JOIN Players ON Players.id = Records.player_id
                WHERE Players.username = ?
                GROUP BY Players.id;"""
    res = await fetch_one(query, [username])
    return res