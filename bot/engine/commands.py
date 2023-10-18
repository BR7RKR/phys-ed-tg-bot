from typing import Optional

from clients.lk import LkClient, WrongUsernameOrPasswordError, ServerError
from clients.phys import PhysEdJournalClient
from clients.tg import TgClient
from abc import ABCMeta, abstractmethod

from clients.tg import Update
from database.models import Student
from engine.constants import START_ANSWER, HELP_ANSWER, REPEATED_REGISTRATION_ANSWER, PROVIDE_PASSWORD_ANSWER, \
    SUCCESSFUL_REGISTRATION_ANSWER, WRONG_LOGIN_DATA_ANSWER, SERVER_ERROR_ANSWER, REGISTRATION_ERROR_ANSWER, \
    REGISTRATION_CONFIRMATION_ERROR_ANSWER, STATS_SEARCH_ERROR_ANSWER
from engine.session import BotSessionsBase, SessionEntity


# Abstract command
class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, upd: Update):
        pass

    @abstractmethod
    def is_for(self, command_definer: Update):
        pass


class HelpCommand(Command):
    def __init__(self, tg_client: TgClient, sessions: BotSessionsBase):
        self._name = "/help"
        self._tg_client = tg_client
        self._sessions = sessions

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, HELP_ANSWER)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        session = self._sessions.get_current_session(command_definer.message.chat.id)
        if session is not None:
            return False

        message = command_definer.message.text
        return self._name == message


class StartCommand(Command):
    def __init__(self, tg_client: TgClient, sessions: BotSessionsBase):
        self._name = "/start"
        self._tg_client = tg_client
        self._login = None
        self._password = None
        self._sessions = sessions

    async def execute(self, upd: Update):
        possible_stud = await Student.get_or_none(user_tg_id=upd.message.from_.id)
        if possible_stud is not None:
            await self._tg_client.send_message(upd.message.chat.id, REPEATED_REGISTRATION_ANSWER)
            return

        await self._tg_client.send_message(upd.message.chat.id, START_ANSWER)

        start_session = SessionEntity()
        start_session.session_name = self._name
        start_session.chat_id = upd.message.chat.id
        start_session.additional_info = {
            'login': '',
            'password': ''
        }
        self._sessions.start(start_session)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        session = self._sessions.get_current_session(command_definer.message.chat.id)
        if session is not None:
            return False

        message = command_definer.message.text
        return self._name == message


class LoginCommand(Command):
    def __init__(self, tg_client: TgClient, sessions: BotSessionsBase, lk_client: LkClient):
        self._tg_client = tg_client
        self._sessions = sessions
        self._session: Optional[SessionEntity] = None
        self._lk_client = lk_client

    async def execute(self, upd: Update):
        if self._session.additional_info['login'] == '':
            self._session.additional_info['login'] = upd.message.text
            await self._tg_client.send_message(upd.message.chat.id, PROVIDE_PASSWORD_ANSWER)
            return

        if self._session.additional_info['password'] == '':
            self._session.additional_info['password'] = upd.message.text

            login = self._session.additional_info['login']
            password = self._session.additional_info['password']

            try:
                token = await self._lk_client.get_token(login, password)
                guid = await self._lk_client.get_guid(token)

                student = Student(user_tg_id=upd.message.from_.id, guid=guid)
                await student.save()

                await self._tg_client.send_message(upd.message.chat.id, SUCCESSFUL_REGISTRATION_ANSWER)
            except WrongUsernameOrPasswordError:
                await self._tg_client.send_message(upd.message.chat.id, WRONG_LOGIN_DATA_ANSWER)
            except ServerError:
                await self._tg_client.send_message(upd.message.chat.id, SERVER_ERROR_ANSWER)
            except Exception:
                await self._tg_client.send_message(upd.message.chat.id, REGISTRATION_ERROR_ANSWER)

            self._sessions.end(self._session)
            return

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        self._session = self._sessions.get_current_session(command_definer.message.chat.id)
        if self._session is None:
            return False

        if self._session.session_name != '/start':
            return False

        return True


class StatsCommand(Command):
    def __init__(self, tg_client: TgClient, sessions: BotSessionsBase, phys_client: PhysEdJournalClient):
        self._name = '/stats'
        self._tg_client = tg_client
        self._sessions = sessions
        self._session: Optional[SessionEntity] = None
        self._phys_client = phys_client

    async def execute(self, upd: Update):
        id = upd.message.from_.id

        student = await Student.get_or_none(user_tg_id=id)
        if student is None:
            await self._tg_client.send_message(upd.message.chat.id, REGISTRATION_CONFIRMATION_ERROR_ANSWER)
            return

        phys_stud = await self._phys_client.get_student(student.guid)

        if phys_stud is None:
            await self._tg_client.send_message(upd.message.chat.id, STATS_SEARCH_ERROR_ANSWER)
            return

        await self._tg_client.send_message(upd.message.chat.id,
                                           f'Вот ваша статистика:\n Баллы всего - {self._calculate_total_points(phys_stud)}'
                                           f'\n Посещения - {phys_stud.visits}'
                                           f'\n Баллы за нормативы - {phys_stud.points_for_standard}'
                                           '\n'
                                           f'\n История посещений: \n{self._form_visit_history(phys_stud)}')

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        session = self._sessions.get_current_session(command_definer.message.chat.id)
        if session is not None:
            return False

        message = command_definer.message.text
        return self._name == message

    def _calculate_total_points(self, student):
        return (student.visits * student.group.visit_value) + student.additional_points + student.points_for_standard

    def _form_visit_history(self, student) -> str:
        res = []
        for v in student.visits_history:
            res.append(f'  ===========\n  Дата - {v.date}\n  Преподаватель - {v.teacher_name}\n  ===========\n \n')

        return ''.join(res)
