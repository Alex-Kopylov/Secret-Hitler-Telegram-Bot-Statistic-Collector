from telegram import Message, Poll


def message_is_poll(msg: Message) -> bool:
    """Check if a message contains a poll"""
    return isinstance(msg.effective_attachment, Poll)


def is_message_from_group_chat(msg: Message) -> bool:
    """Check if a message is from a group chat"""
    return msg.chat.type == "group" or msg.chat.type == "supergroup"


async def try_to_delete_message(context, chat_id, message_id):
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        return
