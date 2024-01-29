from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Check out the [website](https://secrethitler.com/) for more info and to print "
        "out your own copy for free! This Telegram bot is help you to gather statistics "
        "about your games. ",
        parse_mode="Markdown",
    )
