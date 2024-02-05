from telegram.ext import PollAnswerHandler, CommandHandler

from src import handlers
from src.callbacks.receive_poll_answer import receive_poll_answer


def get_handlers() -> tuple:
    return (
        # Command handlers
        CommandHandler("start", handlers.start),
        CommandHandler("help", handlers.help),
        CommandHandler("game", handlers.game),
        CommandHandler("save", handlers.save),
        # Poll answer handler
        PollAnswerHandler(receive_poll_answer),
    )