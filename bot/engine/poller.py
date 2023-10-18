import asyncio
from asyncio import Task
from typing import Optional

from engine.exceptions import MissingTgClientError
from clients.tg import TgClient


class Poller:
    def __init__(self, tg_client: TgClient, queue: asyncio.Queue):
        self.tg_client = tg_client
        self.queue = queue
        self._task: Optional[Task] = None

    async def _worker(self):
        if self.tg_client is None:
            raise MissingTgClientError(Poller.__name__)

        offset = 0
        while True:
            res = await self.tg_client.get_updates_in_objects(offset=offset, timeout=60)
            for u in res.result:
                offset = u.update_id + 1
                print(u)
                await self.queue.put(u)

    async def start(self):
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        self._task.cancel()
