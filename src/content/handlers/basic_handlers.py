import logging
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from repository.crud.test_repo import TestRepo
from repository.models import *
from .keyboards import kb, ikb

import src.content.states as st


router = Router()


@router.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext, session: AsyncSession) -> None:
    current_state = await state.get_state()
    await msg.answer(f"Hi, Im started! Current state is {current_state}")

    test_repo = TestRepo(session)
    tests = await test_repo.find_all()
    for test_obj in tests:
        await msg.answer(test_obj.text)


# States can be set:
# async def set_state(msg: types.Message, state: FSMContext) -> None:
#     await state.set_state(st.SomeState.state1)
