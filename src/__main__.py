"""
Telegram bot entry point.

"""

import logging

from src.callbacks.receive_poll_answer import receive_poll_answer
from src.db import close_db
from src import config
from src import handlers
from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)

from telegram.constants import ParseMode

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler,
)

COMMAND_HANDLERS = {
    "start": handlers.start,
    "help": handlers.help,
}
CALLBACK_QUERY_HANDLERS = {
    # "button": handlers.button,
}
CONVERSATION_HANDLERS = {
    "game": handlers.game,
    "save": handlers.save,
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

if not config.TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN env variable" "wasn't implemented in .env file."
    )


# async def receive_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """On receiving polls, reply to it by a closed poll copying the received poll"""
#
#     actual_poll = update.effective_message.poll
#
#     # Only need to set the question and options, since all other parameters don't matter for
#
#     # a closed poll
#
#     await update.effective_message.reply_poll(
#         question=actual_poll.question,
#         options=[o.text for o in actual_poll.options],
#         # with is_closed true, the poll/quiz is immediately closed
#         is_closed=True,
#         reply_markup=ReplyKeyboardRemove(),
#     )


def main() -> None:
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))
    for conversation_name, conversation_handler in CONVERSATION_HANDLERS.items():
        application.add_handler(
            ConversationHandler(
                entry_points=[CommandHandler(conversation_name, conversation_handler)],
                states={},
                fallbacks=[],
            )
        )
    for callback_query_name, callback_query_handler in CALLBACK_QUERY_HANDLERS.items():
        application.add_handler(CallbackQueryHandler(callback_query_handler))

    # application.add_handler(MessageHandler(filters.POLL, receive_poll))
    application.add_handler(PollAnswerHandler(receive_poll_answer))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
    finally:
        close_db()
