
<img alt="board game logo" src="https://upload.wikimedia.org/wikipedia/en/thumb/8/89/Secret_Hitler.svg/2560px-Secret_Hitler.svg.png" width="300"/>



_Secret Hitler is a social deduction game for 5–10 people about finding and stopping Hitler and a fascist takeover._

Check out the [website](https://secrethitler.com/) for more info and to print out your own copy for free!


This Telegram bot is help you to gather statistics about your games. 


## How to use
1. Add the [Secret Hitler Statistics Bot](t.me/SHStatBot) to your Telegram group chat
2. Start a new game with the `/game` command to record results of the game
3. Ask players to vote
4. Use the `/save` command to save the game results by replaying the game in the chat. Be aware that only the game creator can save the game.


5. **_Displaying Statistics will be available soon_**

### Commands
* **/start** the bot
* **/help** - get help
* **/game** - start a new game
* **/save** - save the current game


* **_Adding new commands for displaying statistics is in progress_**

## Self-hosting bot
To host your own instance of the bot, follow these steps:
1. Clone the repository
2. Install Docker and Docker Compose
3. Create a `.env` file in the root directory with the following content:

```dotenv
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
DEVELOPER_CHAT_ID=your_chat_id_for_getting_logs_and_errors# optional
SQLITE_DB_FILE_PATH=db.sqlite# or any other path that you prefer
```

Please note that you need to create a new bot using the [BotFather](https://t.me/BotFather) and get the token for


## Data we collect
1. Telegram user metadata (username, first name, last name, user id)
2. Game statistics (who created the game poll and who voted for whom)
3. Group chat metadata (chat id, chat title) without any messages

**WE DO NOT COLLECT YOUR MESSAGES**

## Development
Please feel free to contribute to the project. You can create a new issue or a pull request.