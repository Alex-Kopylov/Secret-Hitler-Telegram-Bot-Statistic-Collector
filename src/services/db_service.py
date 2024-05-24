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


async def fetch_user(username=None, id=None, first_name=None, full_name=None, last_name=None):
    # returns full player info by given info
    conditions = []
    if not id is None:
        conditions.append(f'id = {id.__repr__()}')
    if not username is None:
        conditions.append(f'username = {username.__repr__()}')
    if not first_name is None:
        conditions.append(f'first_name = {first_name.__repr__()}')
    if not last_name is None:
        conditions.append(f'last_name = {last_name.__repr__()}')
    if not full_name is None:
        conditions.append(f'full_name = {full_name.__repr__()}')
    query = f"""SELECT * FROM players
                WHERE {' AND '.join(conditions)};"""
    result = await fetch_one(query, [])
    return result
        
        
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


async def fetch_player_answers(user_id):
    """
    Returns table of player with given username results grouped by his answers
    
    Parameters:
    -----------
    cur : sqlite3 cursor
        Cursor to the given database.
    
    user_id : int
        Id of a given player.
    
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
                FROM records
                WHERE records.player_id = ?;"""
    res = await fetch_one(query, [user_id])
    return res


async def fetch_players_stats(order='DESC', mingames=None, top=None):
    """
    Returns table containing number of wins and loses for each role and winrate
    
    Parameters:
    -----------
    order : str values 'DESC' or 'ASC'
    
    top : uint or None
        function returns top number of results, if that's not None  
    
    Retuens:
    --------
    res : DataFrame
        Columns: username, 
                 LW (liberal wins), 
                 FW (fascist wins), 
                 HW (Hitler wins), 
                 LL (liberal loses), 
                 FL (fascist loses), 
                 HL (Hitler loses), 
                 winrate
    """
    if mingames is None:
        condition = ""
    else:
        condition = f"HAVING games >= {mingames}"
    query = f"""SELECT players.id, players.username, players.full_name, 
            SUM(CASE WHEN records.role = 'LW' THEN 1 ELSE 0 END) AS LW,
            SUM(CASE WHEN records.role = 'FW' THEN 1 ELSE 0 END) AS FW,
            SUM(CASE WHEN records.role IN ('HW', 'HC') THEN 1 ELSE 0 END) AS HW,
            SUM(CASE WHEN records.role = 'LL' THEN 1 ELSE 0 END) AS LL,
            SUM(CASE WHEN records.role = 'FL' THEN 1 ELSE 0 END) AS FL, 
            SUM(CASE WHEN records.role IN ('HL', 'HD') THEN 1 ELSE 0 END) AS HL,
            COUNT(records.role) AS games,
            AVG(CASE WHEN records.role IN ('LW', 'FW', 'HW', 'HC') THEN 1 ELSE 0 END) AS winrate
            FROM records
            INNER JOIN players ON players.id = records.player_id
            GROUP BY player_id {condition}
            ORDER BY winrate {order};"""
    if top is not None:
        query = query[:-1] + f'\nLIMIT {top};'
    res = await fetch_all(query, [])
    return res

    
    
async def fetch_result_distribution(playroom_id=None):
    # returns 
    if playroom_id is None:
        condition = ''
    else:
        condition = f'WHERE playroom_id = {playroom_id}'
    query = f"""WITH roles_in_games(Games, FW, LL, LW, FL, HW, HL, CH, DH) AS 
                (SELECT 1 AS Games,
                        SUM(CASE WHEN role = 'FW' THEN 1 ELSE 0 END) > 0 AS FW, 
                        SUM(CASE WHEN role = 'LL' THEN 1 ELSE 0 END) > 0 AS LL, 
                        SUM(CASE WHEN role = 'LW' THEN 1 ELSE 0 END) > 0 AS LW, 
                        SUM(CASE WHEN role = 'FL' THEN 1 ELSE 0 END) > 0 AS FL, 
                        SUM(CASE WHEN role = 'HW' THEN 1 ELSE 0 END) > 0 AS HW, 
                        SUM(CASE WHEN role = 'HL' THEN 1 ELSE 0 END) > 0 AS HL, 
                        SUM(CASE WHEN role = 'CH' THEN 1 ELSE 0 END) > 0 AS CH, 
                        SUM(CASE WHEN role = 'DH' THEN 1 ELSE 0 END) > 0 AS DH
                FROM records
                {condition}
                GROUP BY game_id)
                SELECT SUM(Games) as Games,
                       SUM(FW) AS FW,
                       SUM(LL) AS LL,
                       SUM(LW) AS LW,
                       SUM(FL) AS FL,
                       SUM(HW) AS HW,
                       SUM(HL) AS HL,
                       SUM(CH) AS CH,
                       SUM(DH) AS DH
                FROM roles_in_games;
                """
    result = await fetch_one(query, [])
    return result


async def get_answer_coeffs(playroom_id=None):
    # calculate the coeffs for rating 
    d = await fetch_result_distribution(playroom_id)
    coeffs = {'FW' : 0.5*d['Games']/d['FW'], 
              'LW' : 0.5*d['Games']/d['LW'], 
              'HW' : 0.5*d['Games']/d['HW'], 
              'CH' : 0.5*d['Games']/d['CH'], 
              'FL' : -0.5*d['Games']/d['FL'], 
              'LL' : -0.5*d['Games']/d['LL'], 
              'HL' : -0.5*d['Games']/d['HL'], 
              'DH' : -0.5*d['Games']/d['DH']
    }
    return coeffs


async def get_players_rating(playroom_id=None, order='DESC', mingames=None, top=None):
    """
    Returns table containing number of wins and loses for each role and winrate
    
    Parameters:
    -----------
    playroom_id : int or None
    
    order : str values 'DESC' or 'ASC'
    
    top : uint or None
        function returns top number of results, if that's not None  
    
    Retuens:
    --------
    res : DataFrame
        Columns: username, 
                 LW (liberal wins), 
                 FW (fascist wins), 
                 HW (Hitler wins), 
                 LL (liberal loses), 
                 FL (fascist loses), 
                 HL (Hitler loses), 
                 winrate
    """
    answer_coeffs = await get_answer_coeffs(playroom_id=playroom_id)
    
    if playroom_id is None: condition = ''
    else: condition = f'WHERE playroom_id = {playroom_id}'
    
    if mingames is None: having = ""
    else: having = f"HAVING games >= {mingames}"
    
    query = f"""
            SELECT player_id, players.username, players.full_name, 
            AVG(CASE WHEN role IN ('FW', 'LW', 'HW', 'CH') THEN 1 ELSE 0 END) AS winrate, 
            COUNT(role) AS games,
            SUM(CASE WHEN role = 'FW' THEN {answer_coeffs['FW']}
                     WHEN role = 'LW' THEN {answer_coeffs['LW']}
                     WHEN role = 'HW' THEN {answer_coeffs['HW']}
                     WHEN role = 'CH' THEN {answer_coeffs['CH']}
                     WHEN role = 'FL' THEN {answer_coeffs['FL']}
                     WHEN role = 'LL' THEN {answer_coeffs['LL']}
                     WHEN role = 'HL' THEN {answer_coeffs['HL']}
                     WHEN role = 'DH' THEN {answer_coeffs['DH']} END) AS rating, 
            SUM(CASE WHEN records.role = 'LW' THEN 1 ELSE 0 END) AS LW,
            SUM(CASE WHEN records.role = 'FW' THEN 1 ELSE 0 END) AS FW,
            SUM(CASE WHEN records.role IN ('HW', 'HC') THEN 1 ELSE 0 END) AS HW,
            SUM(CASE WHEN records.role = 'LL' THEN 1 ELSE 0 END) AS LL,
            SUM(CASE WHEN records.role = 'FL' THEN 1 ELSE 0 END) AS FL, 
            SUM(CASE WHEN records.role IN ('HL', 'HD') THEN 1 ELSE 0 END) AS HL
            FROM records
            INNER JOIN players ON players.id = records.player_id
            {condition}
            GROUP BY player_id {having}
            ORDER BY rating {order}
    """
    if top is not None:
        query = query[:-1] + f'\nLIMIT {top};'
    result = await fetch_all(query, [])
    return result
    
    
    
    
    
    
    
async def fetch_connection_stats(username, order='DESC', top=None, which='teammate'):
    """
    Returns table containing number of wins and loses for each role and winrate
    
    Parameters:
    -----------
    username : string from table Players.username
        Username of given player.
        
    order : str values 'DESC' or 'ASC'
    
    top : uint or None
        Function will return top n number of results, if that's not None  
    
    which: str or None
        Define which stats this function will return:
        'teammate' : teammates stats, 
        'opponent' : opponents stats,
        None : full stats
    
    Returns:
    --------
    res : DataFrame
        Columns: username, 
                 LW - Wins playing in liberal team
                 LL - Loses playing in liberal team
                 FW - Wins playing in fascist team
                 FL - Loses playing in fascist team
                 winrate
    """
    query_which = {None: '', 
                   'teammate': "\nAND ((records.role in ('LW', 'LL') AND w.team = 'Liberal') OR (records.role IN ('FW', 'FL', 'HC', 'HL') AND w.team = 'Fascist'))", 
                   'opponent': "\nAND ((records.role in ('LW', 'LL') AND w.team = 'Fascist') OR (records.role IN ('FW', 'FL', 'HC', 'HL') AND w.team = 'Liberal'))"
                  }[which]
    if top is None:
        query_limit = ''
    else:
        query_limit = f'\nLIMIT {top}'
    query = f"""WITH w(game_id, team, result) AS (SELECT records.game_id, 
                CASE WHEN records.role IN ('LL', 'LW') THEN 'Liberal' ELSE 'Fascist' END AS team, 
                CASE WHEN records.role IN ('FW', 'LW', 'HC', 'HW') THEN 'Win' ELSE 'Lose' END AS result
                FROM records INNER JOIN players ON players.id = records.player_id 
                WHERE players.username = ?)
                SElECT players.username, players.full_name, 
                SUM(CASE WHEN team = 'Liberal' AND result = 'Win' THEN 1 ELSE 0 END) AS LW, 
                SUM(CASE WHEN team = 'Fascist' AND result = 'Win' THEN 1 ELSE 0 END) AS FW, 
                SUM(CASE WHEN team = 'Liberal' AND result = 'Lose' THEN 1 ELSE 0 END) AS LL, 
                SUM(CASE WHEN team = 'Fascist' AND result = 'Lose' THEN 1 ELSE 0 END) AS FL, 
                AVG(CASE WHEN result = 'Win' THEN 1 ELSE 0 END) AS Winrate
                FROM records 
                INNER JOIN w ON w.game_id = records.game_id 
                INNER JOIN players ON players.id = records.player_id
                WHERE players.username != ? {query_which}
                GROUP BY records.player_id
                ORDER BY Winrate {order}{query_limit};"""
    
    res = await fetch_all(query, [username, username])
    return res