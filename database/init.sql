-- Create table for players
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_user_id INTEGER,
    username TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT
);

-- Create table for playrooms
CREATE TABLE IF NOT EXISTS playrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_chat_id INTEGER,
    name TEXT NOT NULL
);

-- Create junction table for players and playrooms
CREATE TABLE IF NOT EXISTS players_and_playrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    playroom_id INTEGER,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (playroom_id) REFERENCES playrooms(id)
);

-- Create table for games
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playroom_id INTEGER,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    result TEXT,
    FOREIGN KEY (playroom_id) REFERENCES playrooms(id)
);

-- Create table for records
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    game_id INTEGER,
    role TEXT,
    won INTEGER, -- 0 or 1
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (game_id) REFERENCES games(id)
);

-- Create a trigger to update games table when the first record for a game ends
CREATE TRIGGER IF NOT EXISTS update_game_end_time
AFTER INSERT ON records
FOR EACH ROW
BEGIN
    -- Update the end_time in the games table if it is the first record for the game
    UPDATE games
    SET end_time = CASE
                    WHEN (SELECT COUNT(*) FROM records WHERE game_id = NEW.game_id) = 1
                    THEN CURRENT_TIMESTAMP
                    ELSE end_time
                  END
    WHERE id = NEW.game_id;
END;
