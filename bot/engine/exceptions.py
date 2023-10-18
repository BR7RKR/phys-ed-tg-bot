class MissingTgClientError(Exception):
    def __init__(self, class_name: str):
        message: str = f"Missing tg client in {class_name}"
        super().__init__(message)


class SessionIsBusyError(Exception):
    def __init__(self, session_name):
        message: str = f"Session is busy with {session_name}"
        super().__init__(message)
