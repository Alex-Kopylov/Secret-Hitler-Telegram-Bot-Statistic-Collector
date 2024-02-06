import logging

from telegram import Update
from telegram.ext import ContextTypes


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
    else:
        logging.error(
            "Failed to save poll answer. Usually happens for polls that are sent to the bot before it "
            "started and not updated",
            exc_info=True,
        )
