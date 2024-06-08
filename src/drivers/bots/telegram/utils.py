from .models import TeleBotUser
from telebot.types import Message

__all__ = ["get_user_from"]


def get_user_from(message: Message) -> TeleBotUser:
    """Get user from a telegram message object.

    Args:
        message (Any): A telegram message object.

    Returns:
        TeleBotUser: The user object.
    """
    user = TeleBotUser(
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    return user
