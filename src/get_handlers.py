from telegram.ext import PollAnswerHandler, CommandHandler

from src import handlers
from src.callbacks.poll_callback_receiver import poll_callback_receiver


def get_handlers() -> tuple:
    return (
        # Command handlers
        CommandHandler("start", handlers.start),
        CommandHandler("help", handlers.help),
        CommandHandler("game", handlers.game),
        CommandHandler("save", handlers.save),
        CommandHandler("mystats", handlers.mystats),
        # Poll answer handler
        PollAnswerHandler(poll_callback_receiver),
    )
