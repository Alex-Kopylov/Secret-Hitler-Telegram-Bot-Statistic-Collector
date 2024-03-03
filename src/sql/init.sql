-- Create table for players
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE, -- Telegram user id
    username TEXT NOT NULL, -- Telegram username
    first_name TEXT, -- Telegram first name
    full_name TEXT, -- Telegram full name
    last_name TEXT, -- Telegram last name
    is_bot TEXT NOT NULL DEFAULT 'FALSE', -- Telegram is_bot
    language_code TEXT -- Telegram language code
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
    time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
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

-- Create table for Polls
CREATE TABLE IF NOT EXISTS polls (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE, -- Unique poll id
    message_id INTEGER NOT NULL, -- Corresponding game id from the games table
    chat_id INTEGER NOT NULL, -- Corresponding playroom id from the playrooms table
    chat_name TEXT NOT NULL, -- Name of the chat from the playroom
    creator_id INTEGER NOT NULL, -- Id of the player who created the poll
    creator_username TEXT NOT NULL, -- Username of the player who created the poll
    creation_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (message_id) REFERENCES games(id),
    FOREIGN KEY (chat_id) REFERENCES playrooms(id),
    FOREIGN KEY (creator_id) REFERENCES players(id)
);

-- Create table for Poll Results
CREATE TABLE IF NOT EXISTS poll_results (
    poll_id INTEGER NOT NULL, -- Corresponding poll id from the polls table
    user_id INTEGER NOT NULL, -- Id of the player who answered the poll
    answer TEXT NOT NULL, -- The answer given by the player
    FOREIGN KEY (poll_id) REFERENCES polls(id),
    FOREIGN KEY (user_id) REFERENCES players(id),
    UNIQUE(poll_id, user_id)
);

.quit