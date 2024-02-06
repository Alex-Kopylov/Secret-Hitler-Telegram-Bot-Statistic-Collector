-- Create table for players
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE, -- Telegram user id
    username TEXT NOT NULL, -- Telegram username
    first_name TEXT, -- Telegram first name
    last_name TEXT -- Telegram last name
);

-- Create table for playrooms
CREATE TABLE IF NOT EXISTS playrooms (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE, -- Telegram chat id
    name TEXT NOT NULL
);

-- Create junction table for players and playrooms
CREATE TABLE IF NOT EXISTS players_and_playrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    player_id INTEGER NOT NULL UNIQUE, -- Telegram user id
    playroom_id INTEGER NOT NULL UNIQUE, -- Telegram chat id
    date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (playroom_id) REFERENCES playrooms(id)
);

-- Create table for games
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE, -- Telegram poll id
    playroom_id INTEGER, -- Telegram chat id
    creator_id INTEGER NOT NULL, -- Telegram user id who created the game
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_time DATETIME,
    result TEXT, -- ["Hitler Canceler", "Fascist Law", "Hitler Death", "Liberal Law"]
    FOREIGN KEY (creator_id) REFERENCES players(id),
    FOREIGN KEY (playroom_id) REFERENCES playrooms(id)
);

-- Create table for records
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    creator_id INTEGER NOT NULL, -- Telegram user id who created the record
    player_id INTEGER NOT NULL,
    playroom_id INTEGER, -- Telegram chat id
    game_id INTEGER NOT NULL, -- Telegram poll id
    role TEXT NOT NULL, -- [HC, HD, HL, FL, LL, LW, FW] # TODO: to int category
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (creator_id) REFERENCES players(id),
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (playroom_id) REFERENCES playrooms(id)
);

.quit