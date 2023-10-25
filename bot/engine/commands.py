from logger import logging

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from clients.lk import LkClient, WrongUsernameOrPasswordError, ServerError
from clients.phys import PhysEdJournalClient

from database.models import Student
from engine.base import dp
from engine.constants import START_ANSWER, HELP_ANSWER, REPEATED_REGISTRATION_ANSWER, PROVIDE_PASSWORD_ANSWER, \
    SUCCESSFUL_REGISTRATION_ANSWER, WRONG_LOGIN_DATA_ANSWER, SERVER_ERROR_ANSWER, \
    REGISTRATION_CONFIRMATION_ERROR_ANSWER, STATS_SEARCH_ERROR_ANSWER, RATE_LIMIT_ERROR_ANSWER
from engine.rate_limiter import RateLimiter
from engine.states import RegStudent
from engine.utils import calculate_total_points, form_visit_history


@dp.message(Command('help'))
async def help_command(message: Message, state: FSMContext):
    try:
        if await state.get_state() is not None:
            return

        await message.answer(HELP_ANSWER)
    except Exception as e:
        logging.error(e)


@dp.message(Command('start'))
async def start_command(message: Message, state: FSMContext):
    try:
        if await state.get_state() is not None:
            return

        possible_stud = await Student.get_or_none(user_tg_id=message.from_user.id)
        if possible_stud is not None:
            await message.answer(REPEATED_REGISTRATION_ANSWER)
            return

        await message.answer(START_ANSWER)

        await state.set_state(RegStudent.login)
    except Exception as e:
        logging.error(e)


@dp.message(RegStudent.login)
async def get_login(message: Message, state: FSMContext):
    try:
        await state.update_data(login=message.text)
        await state.set_state(RegStudent.password)
        await message.answer(PROVIDE_PASSWORD_ANSWER)
    except Exception as e:
        logging.error(e)


@dp.message(RegStudent.password)
async def get_password(message: Message, state: FSMContext):
    try:
        await state.update_data(password=message.text)
        state_data = await state.get_data()
        await state.clear()

        login = state_data['login']
        password = state_data['password']

        lk_client: LkClient = dp['lk_client']

        token = await lk_client.get_token(login, password)
        guid = await lk_client.get_guid(token)

        student = Student(user_tg_id=message.from_user.id, guid=guid)
        await student.save()

        await message.answer(SUCCESSFUL_REGISTRATION_ANSWER)
    except WrongUsernameOrPasswordError as e:
        await message.answer(WRONG_LOGIN_DATA_ANSWER)
        logging.error(e)
    except ServerError as e:
        await message.answer(SERVER_ERROR_ANSWER)
        logging.critical(e)
    except Exception as e:
        logging.error(e)


@dp.message(Command('stats'))
async def stats_command(message: Message, state: FSMContext):
    try:
        if await state.get_state() is not None:
            return

        rate_limiter: RateLimiter = dp['rate_limiter']
        phys_client: PhysEdJournalClient = dp['phys_client']
        id = message.from_user.id

        if not rate_limiter.has_free_requests(id):
            await message.answer(RATE_LIMIT_ERROR_ANSWER)
            return

        student = await Student.get_or_none(user_tg_id=id)
        if student is None:
            await message.answer(REGISTRATION_CONFIRMATION_ERROR_ANSWER)
            return

        phys_stud = await phys_client.get_student(student.guid)

        if phys_stud is None:
            await message.answer(STATS_SEARCH_ERROR_ANSWER)
            return

        await message.answer(f'Вот ваша статистика:\n Баллы всего - {calculate_total_points(phys_stud)}'
                             f'\n Посещения - {phys_stud.visits}'
                             f'\n Баллы за нормативы - {phys_stud.points_for_standard}'
                             '\n'
                             f'\n История посещений: \n{form_visit_history(phys_stud)}')

        rate_limiter.add_request(id)
    except Exception as e:
        logging.error(e)
