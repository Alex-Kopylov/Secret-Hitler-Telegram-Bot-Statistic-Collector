import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from src.services.draw_graphs import draw_user_winrate
from src.config import AppConfig


async def mystats(
    update: Update, context: ContextTypes.DEFAULT_TYPE, config: AppConfig = AppConfig()
) -> None:
    # Draws personal stats of asking user
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    try:
        await context.bot.send_photo(chat_id=chat_id,
                                     photo=await draw_user_winrate(user_id, context=context), 
                                     disable_notification=True)
        #await update.effective_message.delete()
    except TelegramError as e:
        logging.error(f"Failed to send photo: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Sorry, there was an error processing your request.")