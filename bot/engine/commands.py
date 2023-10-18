from clients.tg import CallBackData, TgClient
from abc import ABCMeta, abstractmethod

from clients.tg import Update
from engine.constants import START_ANSWER, HELP_ANSWER


# Abstract command
class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, upd: Update):
        pass

    @abstractmethod
    def is_for(self, command_definer: Update):
        pass


class HelpCommand(Command):
    def __init__(self, tg_client: TgClient):
        self._name = "/help"
        self._tg_client = tg_client

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, HELP_ANSWER)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        message = command_definer.message.text
        return self._name == message


class TestCommand(Command):
    def __init__(self, tg_client: TgClient):
        self._name = "/test"
        self._tg_client = tg_client

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, upd.message.text)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        message = command_definer.message.text
        return self._name == message


class StartCommand(Command):
    def __init__(self, tg_client: TgClient):
        self._name = "/start"
        self._tg_client = tg_client

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, START_ANSWER)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        message = command_definer.message.text
        return self._name == message
