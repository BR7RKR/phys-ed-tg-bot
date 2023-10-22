import inspect

from clients.lk import LkClient
from clients.phys import PhysEdJournalClient
from clients.tg import Update, TgClient
from engine import commands
from engine.rate_limiter import RateLimiter
from engine.session import BotSessionsBase


class CommandDistributor:
    def __init__(self, tg_client: TgClient, session: BotSessionsBase, lk_client: LkClient, phys_client: PhysEdJournalClient, rate_limiter: RateLimiter):
        self._tg_client = tg_client
        self._session = session
        self._lk_client = lk_client
        self._phys_client = phys_client
        self._rate_limiter = rate_limiter
        self._commands = self._set_commands()

    async def execute(self, upd: Update):
        command = await self._define_command(upd)

        if command is None:
            return

        try:
            await command.execute(upd)
        except Exception as e:
            print(e)
            return

    async def _define_command(self, command_definer) -> commands.Command:
        for com in self._commands:
            if com.is_for(command_definer):
                return com

    def _set_commands(self):
        command_list = []
        for cls in commands.__dict__.values():
            if isinstance(cls, type) and issubclass(cls, commands.Command) and cls != commands.Command:
                constructor = cls.__init__
                params = inspect.signature(constructor).parameters
                args = []

                for param in params.values():
                    if param.name == 'self':
                        continue
                    if param.annotation == TgClient:
                        args.append(self._tg_client)
                        continue
                    if param.annotation == LkClient:
                        args.append(self._lk_client)
                        continue
                    if param.annotation == BotSessionsBase:
                        args.append(self._session)
                        continue
                    if param.annotation == PhysEdJournalClient:
                        args.append(self._phys_client)
                        continue
                    if param.annotation == RateLimiter:
                        args.append(self._rate_limiter)
                        continue
                    else:
                        raise Exception("param's type not defined")

                command_list.append(cls(*args))

        return command_list
