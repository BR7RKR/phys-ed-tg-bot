class WrongUsernameOrPasswordError(Exception):
    def __init__(self):
        message: str = "Wrong username or password"
        super().__init__(message)


class ServerError(Exception):
    def __init__(self, message):
        super().__init__(message)
