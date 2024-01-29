from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def receive_poll_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Summarize a users poll vote"""
    answer = update.poll_answer
    if not answer.option_ids:
        return  # It's retake poll action, ignore it
    if context.bot_data:
        answered_poll = context.bot_data[answer.poll_id]
        record = {
            "user_id": update.effective_user.id,
            "poll_id": answered_poll["chat_id"],
            "answer": answered_poll["questions"][answer.option_ids[0]],
        }
        await context.bot.send_message(
            text=str(record), chat_id=answered_poll["chat_id"]
        )
    else:
        # failed to save poll answer.
        # Ussually happens for polls that are sent to the bot before it started and not updated
        # TODO save polls to db and query them instead saving them to bot_data
        return
