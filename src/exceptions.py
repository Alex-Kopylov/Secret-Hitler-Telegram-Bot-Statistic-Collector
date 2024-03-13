class GroupChatRequiredException(Exception):
    """Exception raised when an attempt is made to start a game outside a group chat."""

    def __init__(self, user_id, message="Game can only be started in a group chat."):
        self.user_id = user_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} User ID: {self.user_id}"
