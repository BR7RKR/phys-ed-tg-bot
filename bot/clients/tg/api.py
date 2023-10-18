from io import IOBase
from typing import Optional, Union

from aiohttp import FormData

from clients.tg.dcs import GetUpdatesResponse, SendMessageResponse, SendAudioResponse, SendPhotoResponse, \
    SendVideoResponse, EditMessageReplyMarkupResponse


class TgClient:
    def __init__(self, session, token):
        self._session = session
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    async def get_me(self) -> dict:
        url = self.get_url("getMe")
        async with self._session.get(url) as resp:
            return await resp.json()

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        url = self.get_url("getUpdates")
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout
        async with self._session.get(url, params=params) as resp:
            return await resp.json()

    async def get_updates_in_objects(self, offset: Optional[int] = None, timeout: int = 0) -> GetUpdatesResponse:
        res_dict = await self.get_updates(offset=offset, timeout=timeout)
        return GetUpdatesResponse.Schema().load(res_dict)

    async def send_message(self, chat_id: int, text: str, has_protected_content: Optional[bool] = False) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        payload = {
            'chat_id': chat_id,
            'text': text,
            'has_protected_content': has_protected_content
        }
        async with self._session.post(url, json=payload) as resp:
            res_dict = await resp.json()
            return SendMessageResponse.Schema().load(res_dict)

    async def send_audio(self, chat_id: int, audio: Union[IOBase, str]) -> SendAudioResponse:
        url = self.get_url("sendAudio")
        data = FormData()
        data.add_field('chat_id', str(chat_id))
        data.add_field('audio', audio)
        async with self._session.post(url, data=data) as resp:
            res_dict = await resp.json()
            return SendAudioResponse.Schema().load(res_dict)

    async def send_video(self, chat_id: int, video: Union[IOBase, str]) -> SendVideoResponse:
        url = self.get_url("sendVideo")
        data = FormData()
        data.add_field('chat_id', str(chat_id))
        data.add_field('video', video)
        async with self._session.post(url, data=data) as resp:
            res_dict = await resp.json()
            return SendVideoResponse.Schema().load(res_dict)

    async def send_photo(self, chat_id: int, photo: Union[IOBase, str], caption: Optional[str] = None, reply_markup: Optional = None, protect_content: Optional[bool] = False) -> SendPhotoResponse:
        url = self.get_url("sendPhoto")
        data = FormData()
        data.add_field('chat_id', str(chat_id))
        data.add_field('photo', photo)
        data.add_field('protected_content', protect_content)

        if caption is not None:
            data.add_field('caption', caption)
        if reply_markup is not None:
            data.add_field('reply_markup', reply_markup)

        async with self._session.post(url, data=data) as resp:
            res_dict = await resp.json()
            return SendPhotoResponse.Schema().load(res_dict)

    async def edit_message_reply_markup(self, chat_id: Optional[Union[int, str]] = None, message_id: Optional[int] = None, inline_message_id: Optional[str] = None, reply_markup: Optional = None) -> EditMessageReplyMarkupResponse:
        url = self.get_url("editMessageReplyMarkup")
        data = FormData()

        if chat_id is not None:
            data.add_field('chat_id', str(chat_id))
        if message_id is not None:
            data.add_field('message_id', message_id)
        if inline_message_id is not None:
            data.add_field('inline_message_id', inline_message_id)
        if reply_markup is not None:
            data.add_field('reply_markup', reply_markup)

        async with self._session.post(url, data=data) as resp:
            res_dict = await resp.json()
            return EditMessageReplyMarkupResponse.Schema().load(res_dict)
