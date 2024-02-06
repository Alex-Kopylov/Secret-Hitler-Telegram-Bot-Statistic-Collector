import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.data_models.Player import Player
from src.services.db_service import save_player


async def receive_poll_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # TODO save polls to db and query them instead saving them to bot_data
    """Summarize a users poll vote"""
    answer = update.poll_answer
    if not answer.option_ids:  # Poll retract, delete previous vote
        del context.bot_data[answer.poll_id]["results"][update.effective_user.id]
        return
    if context.bot_data:
        answered_poll = context.bot_data[answer.poll_id]
        user_id = update.effective_user.id
        result = answered_poll["questions"][answer.option_ids[0]]
        context.bot_data[answer.poll_id]["results"][user_id] = result
        await save_player(
            Player(
                telegram_user_id=user_id,
                username=update.effective_user.username,
                first_name=update.effective_user.first_name,
                full_name=update.effective_user.full_name,
                last_name=update.effective_user.last_name,
                is_bot=update.effective_user.is_bot,
                language_code=update.effective_user.language_code,
            )
        )
    else:
        logging.error(
            "Failed to save poll answer. Usually happens for polls that are sent to the bot before it "
            "started and not updated",
            exc_info=True,
        )
