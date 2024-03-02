import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from src.config import AppConfig
from src.data_models.Game import Game
from src.data_models.Record import Record
from src.services.db_service import (
    save_record,
    save_game,
    fetch_poll_data,
    fetch_poll_results,
)
from src.services.draw_result_image import draw_result_image
from src.utils import message_is_poll, is_message_from_group_chat


async def _pass_checks(
    msg_with_poll, update, context
) -> bool:  # TODO async checks and move somewhere else
    # check reply msg exists
    if not msg_with_poll:
        await update.effective_message.reply_text(
            "You will record result by replying to my poll. Have you started the game by /game command?"
        )
        return False
    # check reply msg is from group chat
    if not is_message_from_group_chat(msg_with_poll):
        await update.effective_message.reply_text(
            "You can only save game in a group chat where other players can see the results."
        )
        return False
    # check reply msg is a poll
    if not message_is_poll(msg_with_poll):
        await update.effective_message.reply_text(
            "Please reply to a poll to stop and record results."
        )
        return False

    poll_data = await fetch_poll_data(msg_with_poll.poll.id)
    if not poll_data:
        await update.effective_message.reply_text(
            "Could not find the poll information in the database."
        )
        return False

    if update.effective_user.id != poll_data.creator_id:
        await update.effective_message.reply_text(
            f"You are not the creator of the game! Only @{poll_data['creator_username']} can stop this poll."
        )
        return False

    if update.effective_chat.id != poll_data.chat_id:
        await update.effective_message.reply_text(
            "You can only save the game in the group chat where the poll was created."
        )
        return False

    return True


async def save(
    update: Update, context: ContextTypes.DEFAULT_TYPE, config: AppConfig = AppConfig()
) -> None:
    msg_with_poll = update.effective_message.reply_to_message
    if await _pass_checks(msg_with_poll=msg_with_poll, update=update, context=context):
        await context.bot.stop_poll(update.effective_chat.id, msg_with_poll.message_id)
        poll_id = int(msg_with_poll.poll.id)
        poll_data, poll_results = await asyncio.gather(
            fetch_poll_data(poll_id), fetch_poll_results(poll_id)
        )

        records = [
            Record(
                creator_id=poll_data.creator_id,
                player_id=results.user_id,
                playroom_id=poll_data.chat_id,
                game_id=poll_data.message_id,
                role=results.get_answer_as_text(),
            )
            for results in poll_results
        ]

        game = Game(
            poll_id=poll_data.message_id,
            chat_id=poll_data.chat_id,
            creator_id=poll_data.creator_id,
            results=poll_results,
        )

        # Execute post-game tasks
        await asyncio.gather(
            save_game(game),
            *(save_record(record) for record in records),
            context.bot.delete_message(chat_id=game.chat_id, message_id=game.poll_id),
            update.effective_message.delete(),
            context.bot.send_photo(
                chat_id=game.chat_id,
                photo=await draw_result_image(
                    records=records, result=game.results, update=update, context=context
                ),
                caption="The Game has been saved!",
                disable_notification=True,
            ),
        )
    else:
        await update.effective_message.reply_text(
            "Something went wrong. Can't process your request."
        )
