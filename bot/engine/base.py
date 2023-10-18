import asyncio
from typing import Optional

import aiohttp
from aiohttp import ClientSession

import database.body
from clients.lk import LkClient
from clients.phys import PhysEdJournalClient
from engine.distributor import CommandDistributor
from engine.poller import Poller
from engine.session import BotSessionsBase
from engine.worker import Worker
from clients.tg import TgClient


class Bot:
    def __init__(self, token: str, worker_count: int):
        self._queue = asyncio.Queue()
        self._token = token
        self._session: Optional[ClientSession] = None
        self._lk_session: Optional[ClientSession] = None
        self._phys_session: Optional[ClientSession] = None
        self._tg_client = None
        self._poller = None
        self._worker = None
        self._worker_count = worker_count
        self._db = database.body.Setup()
        self._bot_session = BotSessionsBase()
        self._lk_client = None
        self._phys_client = None

    async def start(self):
        self._session = aiohttp.ClientSession()
        self._lk_session = aiohttp.ClientSession()
        self._phys_session = aiohttp.ClientSession()
        self._tg_client = TgClient(self._session, self._token)
        self._lk_client = LkClient(self._lk_session)
        self._phys_client = PhysEdJournalClient(self._phys_session)
        self._poller = Poller(self._tg_client, self._queue)
        self._worker = Worker(self._queue,
                              self._worker_count,
                              CommandDistributor(self._tg_client,
                                                 self._bot_session,
                                                 self._lk_client,
                                                 self._phys_client
                                                 )
                              )

        await self._db.connect()
        await self._poller.start()
        await self._worker.start()

    async def stop(self):
        await self._db.close()
        await self._poller.stop()
        await self._worker.stop()
        await self._session.close()
        await self._lk_session.close()
        await self._phys_session.close()
