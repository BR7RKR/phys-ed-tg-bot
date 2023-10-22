import asyncio
from typing import List

from clients.tg import Update
from engine.distributor import CommandDistributor


class Worker:
    def __init__(self, queue: asyncio.Queue, concurrent_workers: int, command_distributor: CommandDistributor):
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []
        self._command_distributor = command_distributor

    async def handle_update(self, upd: Update):
        await self._command_distributor.execute(upd)

    async def _worker(self):
        while True:
            upd = await self.queue.get()
            try:
                await self.handle_update(upd)
            finally:
                self.queue.task_done()

    async def start(self):
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]

    async def stop(self):
        await self.queue.join()
        for t in self._tasks:
            t.cancel()
