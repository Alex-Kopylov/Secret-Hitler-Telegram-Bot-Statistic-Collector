import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from src.services.draw_graphs import draw_user_winrate
from src.config import AppConfig


async def mystats(
    update: Update, context: ContextTypes.DEFAULT_TYPE, config: AppConfig = AppConfig()
) -> None:
    # Draws personal stats of asking user
    username = update.effective_user.username
    chat_id =  update.my_chat_member
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=await draw_user_winrate(username), 
                                 disable_notification=True)
    #await update.effective_message.delete()