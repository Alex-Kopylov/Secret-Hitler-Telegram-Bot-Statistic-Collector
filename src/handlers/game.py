from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.utils import message_is_poll, is_message_from_group_chat


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a predefined poll"""

    questions = [
        "I'm canceler Hitler",
        "I'm dead Hitler",
        "I'm Hitler Loser",
        "I'm Liberal Winner",
        "I'm Liberal Loser",
        "I'm Fascistic Winner",
        "I'm Fascistic Loser",
    ]

    message = await context.bot.send_poll(
        update.effective_chat.id,
        f"@{update.effective_user.username} want you to record last game. Please choose your outcome:",
        questions,
        is_anonymous=False,
        allows_multiple_answers=False,
        disable_notification=True,
    )

    # Save some info about the poll the bot_data for later use in receive_poll_answer
    game_metadata = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.id,
            "chat_id": update.effective_chat.id,
            "chat_name": update.effective_chat.title,
            "creator_id": update.effective_user.id,
            "results": {},
        }
    }

    context.bot_data.update(game_metadata)


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # TODO move to separate file
    """Saves a game
    Replying /save to the poll message (created by the bot) stops the poll
    It can only be done by the creator of the poll
    Save poll results
    """

    msg_with_poll = (
        update.effective_message.reply_to_message
    )  # get a poll from reply message

    # check reply msg exists
    if not msg_with_poll:
        await update.effective_message.reply_text(
            "You will record result by replying to my poll. Have you started the game by /game command?"
        )
    # check reply msg is from group chat
    if not is_message_from_group_chat(msg_with_poll):
        await update.effective_message.reply_text(
            "You can only save game in a group chat where other players can see the results."
        )
    # check reply msg is a poll
    if not message_is_poll(msg_with_poll):
        await update.effective_message.reply_text(
            "Please reply to a poll to stop and record results."
        )
    # check reply msg is from the bot
    if msg_with_poll.from_user.id != context.bot.id:
        await update.effective_message.reply_text(
            f"Please reply to poll created by me @{context.bot.username}."
        )
    # check user is creator of the poll
    if (
        update.effective_user.id
        != context.bot_data[msg_with_poll.poll.id]["creator_id"]
    ):
        await update.effective_message.reply_text(
            f"You are not the creator of the game!"
            f"Only {context.bot_data[update.poll.id]['creator_id']} can stop this poll."
        )
    if update.effective_chat.id != context.bot_data[msg_with_poll.poll.id]["chat_id"]:
        await update.effective_message.reply_text(
            f"You can only save game in a group chat where other players can see the results."
        )

    await context.bot.stop_poll(
        update.effective_chat.id, msg_with_poll.id
    )
    poll_results = context.bot_data[msg_with_poll.poll.id]["results"]
    await update.effective_message.reply_text(
        "Poll stopped. Results: {}".format(poll_results)
    )
