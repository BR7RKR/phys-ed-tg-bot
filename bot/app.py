import asyncio
import datetime

from engine.base import TgBot


def run():
    loop = asyncio.get_event_loop()
    bot = TgBot()
    try:
        print('engine has started')
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nstopping", datetime.datetime.now())
        loop.run_until_complete(bot.stop())
        print('engine has been stopped', datetime.datetime.now())



if __name__ == "__main__":
    run()
