class MissingTgClientError(Exception):
    def __init__(self, class_name: str):
        message: str = f"Missing tg client in {class_name}"
        super().__init__(message)
        

class RateLimitError(Exception):
    def __init__(self):
        super().__init__('Request limit exceeded')
