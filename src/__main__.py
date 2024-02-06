"""
Telegram bot entry point.

"""
import logging
import traceback

from telegram.ext import (
    Application,
)

from src import config
from src import handlers
from src.db import close_db
from src.get_handlers import get_handlers


def main() -> None:
    if not config.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN env variable" "wasn't purposed.")

    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
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
