import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from src.data_models.Poll import Poll
from src.data_models.Playroom import Playroom
from src.services.db_service import save_playroom, save_poll
from src.config import AppConfig


async def game(
    update: Update, context: ContextTypes.DEFAULT_TYPE, config: AppConfig = AppConfig()
) -> None:
    """Sends a predefined poll and saves its metadata to the database."""

    questions = config.game_poll_outcomes

    message = await context.bot.send_poll(
        update.effective_chat.id,
        f"@{update.effective_user.username} wants you to record the last game. Please choose your outcome:",
        questions,
        is_anonymous=False,
        allows_multiple_answers=False,
        disable_notification=True,
    )
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
            update.effective_message.delete(),
        ]
    )
