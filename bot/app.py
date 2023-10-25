import asyncio
import datetime

from logger import logging
from engine.base import TgBot


def run():
    loop = asyncio.get_event_loop()
    bot = TgBot()

    start_message = 'engine has started'

    try:
        logging.info(start_message)
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        stop_at_time = f"stopping {datetime.datetime.now()}"
        logging.info(stop_at_time)
        loop.run_until_complete(bot.stop())
        stop_message = f'engine has been stopped {datetime.datetime.now()}'
        logging.info(stop_message)


if __name__ == "__main__":
    run()
