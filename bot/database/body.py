from tortoise import Tortoise


class Setup:
    async def connect(self):
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['database.models']}
        )

        await Tortoise.generate_schemas(safe=True)

    async def close(self):
        await Tortoise.close_connections()
