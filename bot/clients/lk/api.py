from aiohttp import FormData

from clients.lk.exceptions import WrongUsernameOrPasswordError, ServerError


class LkClient:
    def __init__(self, session):
        self._session = session

    def get_url(self):
        return f"https://e.mospolytech.ru/old/lk_api.php"

    async def get_token(self, login, password) -> str:
        url = self.get_url()
        params = {'ulogin': login, 'upassword': password}
        data = FormData(params)

        async with self._session.post(url, data=data) as resp:
            if resp.status == 400:
                raise WrongUsernameOrPasswordError()
            if resp.status != 200:
                raise ServerError("Something went wrong")

            resp_json = await resp.json()
            token = resp_json['token']
            return token

    async def get_guid(self, token) -> str:
        url = self.get_url() + f"/?getAppData&token={token}"

        async with self._session.post(url) as resp:
            if resp.status != 200:
                raise ServerError("Something went wrong")

            resp_json = await resp.json()
            return resp_json['guid_person']
