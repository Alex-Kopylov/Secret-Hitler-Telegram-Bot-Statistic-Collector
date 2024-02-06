from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src import config
from src.data_models.Playroom import Playroom
from src.services.db_service import save_playroom
from src.utils import message_is_poll, is_message_from_group_chat


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a predefined poll"""

    questions = config.GAME_POLL_OUTCOMES

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
            "message_id": message.id,  # will be game_id
            "chat_id": update.effective_chat.id,
            "chat_name": update.effective_chat.title,
            "creator_id": update.effective_user.id,
            "creator_username": update.effective_user.username,
            "results": {},
        }
    }
    await save_playroom(
        Playroom(
            telegram_chat_id=update.effective_chat.id, name=update.effective_chat.title
        )
    )
    context.bot_data.update(game_metadata)
