import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.data_models.Player import Player
from src.data_models.PollResult import PollResult
from src.services.db_service import save_player, save_poll_result, delete_poll_result


async def poll_callback_receiver(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Save or delete poll results in the database."""
    answer = update.poll_answer
    user_id = update.effective_user.id
    poll_id = int(answer.poll_id)  # Convert from telegram string id to int

    if not answer.option_ids:  # Poll retraction, delete previous vote
        await delete_poll_result(poll_id=poll_id, user_id=user_id)
        return

    # Retrieve the selected option's text or index
    selected_option_index = answer.option_ids[0]

    await save_poll_result(
        PollResult(
            poll_id=poll_id,
            user_id=user_id,
            answer=selected_option_index,
        )
    )
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
