import json


class InlineKeyboardButton:
    def __init__(self, text, callback_data):
        self.json = {"text": text, "callback_data": callback_data}


class InlineKeyboard:
    @property
    def keys(self):
        return self._keys

    @property
    def reply_markup(self):
        if self._keys.count == 0:
            return json.dumps({
                'inline_keyboard': []
            })

        return json.dumps({
            'inline_keyboard': [self._keys]
        })

    def __init__(self):
        self._keys = []

    def add_button(self, button: InlineKeyboardButton):
        self._keys.append(button.json)
        return self
