from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.utils import message_is_poll, is_message_from_group_chat


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a predefined poll"""

    questions = [
        "I'm canceler Hitler",
        "I'm dead Hitler",
        "I'm Hitler Loser",
        "I'm Liberal Winner",
        "I'm Liberal Loser",
        "I'm Fascistic Winner",
        "I'm Fascistic Loser",
    ]

    message = await context.bot.send_poll(
        update.effective_chat.id,
        f"@{update.effective_user.username} want you to record last game. Please choose your outcome:",
        questions,
        is_anonymous=False,
        allows_multiple_answers=False,
        disable_notification=True,
    )

    # Save some info about the poll the bot_data for later use in receive_poll_answer
    game_metadata = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.id,
            "chat_id": update.effective_chat.id,
            "chat_name": update.effective_chat.title,
            "creator_id": update.effective_user.id,
            "creator_username": update.effective_user.username,
            "results": {},
        }
    }

    context.bot_data.update(game_metadata)
