import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from src.data_models.Poll import Poll
from src.data_models.Playroom import Playroom
from src.exceptions import GroupChatRequiredException
from src.services.db_service import save_playroom, save_poll
from src.config import AppConfig
from src.utils import is_message_from_group_chat, try_to_delete_message


async def game(
    update: Update, context: ContextTypes.DEFAULT_TYPE, config: AppConfig = AppConfig()
) -> None:
    """Sends a predefined poll and saves its metadata to the database."""

    if not is_message_from_group_chat(update.effective_message):
        await update.effective_message.reply_text(
            "You can only start a game in a group chat.\nPlease add me to a group chat and try again."
        )
        raise GroupChatRequiredException(user_id=update.effective_user.id)

    questions = config.game_poll_outcomes
    message = None
    try:
        message = await context.bot.send_poll(
            update.effective_chat.id,
            f"@{update.effective_user.username} wants you to record the last game. Please choose your outcome:",
            questions,
            is_anonymous=False,
            allows_multiple_answers=False,
            disable_notification=True,
        )
    except Exception as e:
        await update.effective_message.reply_text(
            f"The bot need permission to create Telegram Polls to start a game\n"
            f"Please grant those permissions in chat settings."
        )
        return

    await asyncio.gather(
        *[
            save_poll(
                Poll(
                    id=message.poll.id,
                    message_id=message.message_id,  # Assuming this maps to the Poll table's message_id
                    chat_id=update.effective_chat.id,
                    chat_name=update.effective_chat.title,
                    creator_id=update.effective_user.id,
                    creator_username=update.effective_user.username,
                )
            ),
            save_playroom(
                Playroom(
                    telegram_chat_id=update.effective_chat.id,
                    name=update.effective_chat.title,
                )
            ),
        ]
    )
    await try_to_delete_message(
        context=context,
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.id,
    )
