"""
Telegram bot entry point.

"""

import logging
import traceback

from telegram.ext import (
    Application,
)

from src.config import AppConfig
from src import handlers
from src.db import close_db
from src.get_handlers import get_handlers


async def post_init(application: Application, config: AppConfig = AppConfig()):
    await application.bot.set_my_commands(commands=config.commands)


def main(config: AppConfig = AppConfig()) -> None:
    if not config.telegram_bot_token:
        raise ValueError("telegram_bot_token env variable" "wasn't purposed.")

    application = (
        Application.builder()
        .token(config.telegram_bot_token)
        .post_init(post_init)
        .build()
    )
    application.add_handlers(get_handlers())
    application.add_error_handler(handlers.error_handler)
    # send a message to the developer when the bot is ready
    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        logger = logging.getLogger()
        logger.warning(traceback.format_exc())
    finally:
        close_db()
