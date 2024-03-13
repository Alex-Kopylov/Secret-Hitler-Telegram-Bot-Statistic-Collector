from telegram import Update
from telegram.ext import ContextTypes

from src.config import AppConfig


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE, config: AppConfig = AppConfig()
) -> None:
    """Inform user about what this bot can do"""
    await update.message.reply_text(
        "Hi this bot will help you to gather statistics about your games. Add it to a chat "
        "with your friends and start a game by **/game** command. After game is finished, "
        "stop the poll by **/save** command. You can also /help to get more info."
        "**Hint**: Give the bot admin rights to delete messages and it will automatically clean up after itself.\n"
        "Feel free to contribute to the project: [GitHub]("
        "https://github.com/Alex-Kopylov/Secret-Hitler-Telegram-Bot-Statistic-Collector)\n"
        "Please report any issues to [GitHub Issues]("
        "https://github.com/Alex-Kopylov/Secret-Hitler-Telegram-Bot-Statistic-Collector/issues)",
        parse_mode="Markdown",
    )
