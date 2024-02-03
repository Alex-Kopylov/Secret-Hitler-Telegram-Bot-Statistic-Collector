"""
Telegram bot entry point.

"""

import logging
from typing import Type

from telegram import (
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    PollAnswerHandler,
)
from telegram.ext import BaseHandler

from src import config
from src import handlers
from src.callbacks.receive_poll_answer import receive_poll_answer
from src.db import close_db, get_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_handlers() -> list:
    commands = [
        CommandHandler("start", handlers.start),
        CommandHandler("help", handlers.help),
        CommandHandler("game", handlers.game),
        CommandHandler("save", handlers.save),
    ]
    poll_answer_handler = [
        PollAnswerHandler(receive_poll_answer),
    ]

    return commands + poll_answer_handler


def main() -> None:
    if not config.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN env variable" "wasn't porpoused.")

    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    application.add_handlers(get_handlers())

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
    finally:
        close_db()
