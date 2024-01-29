from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""

    await update.message.reply_text(
        "Hi this bot will help you to gather statistics about your games. Add it to chat "
        "with your friends and start a game by /game command. After game is finished, "
        "stop the poll by /save command. You can also /help to get more info."
    )
