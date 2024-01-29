from telegram import Message, Poll


def message_is_poll(msg: Message) -> bool:
    """Check if a message contains a poll"""
    return isinstance(msg.effective_attachment, Poll)


def is_message_from_group_chat(msg: Message) -> bool:
    """Check if a message is from a group chat"""
    return msg.chat.type in ("group", "supergroup")
