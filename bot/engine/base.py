from typing import Optional

import aiohttp
from aiogram import Bot, Dispatcher
from aiohttp import ClientSession

import config
import database.body
from clients.lk import LkClient
from clients.phys import PhysEdJournalClient
from engine.rate_limiter import RateLimiter

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


class TgBot:
    def __init__(self):
        self._lk_session: Optional[ClientSession] = None
        self._phys_session: Optional[ClientSession] = None
        self._db = database.body.Setup()
        self._lk_client = None
        self._phys_client = None
        self._rate_limiter = RateLimiter()

    async def start(self):
        self._lk_session = aiohttp.ClientSession()
        self._phys_session = aiohttp.ClientSession()
        self._lk_client = LkClient(self._lk_session)
        self._phys_client = PhysEdJournalClient(self._phys_session)

        dp['lk_client'] = self._lk_client
        dp['phys_client'] = self._phys_client
        dp['rate_limiter'] = self._rate_limiter

        await self._db.connect()
        await dp.start_polling(bot)

    async def stop(self):
        await self._db.close()
        await self._lk_session.close()
        await self._phys_session.close()
        await dp.stop_polling()
