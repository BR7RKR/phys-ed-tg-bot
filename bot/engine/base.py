import asyncio
from typing import Optional

import aiohttp
from aiohttp import ClientSession

from engine.distributor import CommandDistributor
from engine.poller import Poller
from engine.worker import Worker
from clients.tg import TgClient


class Bot:
    def __init__(self, token: str, worker_count: int):
        self._queue = asyncio.Queue()
        self._token = token
        self._session: Optional[ClientSession] = None
        self._tg_client = None
        self._poller = None
        self._worker = None
        self._worker_count = worker_count

    async def start(self):
        self._session = aiohttp.ClientSession()
        self._tg_client = TgClient(self._session, self._token)
        self._poller = Poller(self._tg_client, self._queue)
        self._worker = Worker(self._queue, self._worker_count, CommandDistributor(self._tg_client))
        await self._poller.start()
        await self._worker.start()

    async def stop(self):
        await self._poller.stop()
        await self._worker.stop()
        await self._session.close()
