import json
import logging
import traceback
import html

from telegram import Update
from telegram.constants import ParseMode

from src.config import AppConfig

from telegram.ext import ContextTypes


async def error_handler(
    update: object, context: ContextTypes.DEFAULT_TYPE, config: AppConfig = AppConfig()
) -> None:
    # set a higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 characters limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    if config.developer_chat_id:
        # Finally, send the message
        await context.bot.send_message(
            chat_id=config.developer_chat_id, text=message, parse_mode=ParseMode.HTML
        )
    else:
        logger.error(
            "developer_chat_id env variable wasn't purposed. Please set it to your chat id if you want to "
            "receive error messages in telegram chat."
        )
