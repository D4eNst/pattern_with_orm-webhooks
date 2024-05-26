from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from repository.crud.users import UserRepo

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext, session: AsyncSession) -> None:
    current_state = await state.get_state()
    await msg.answer(f"Hi, Im started! Current state is {current_state}")

    test_repo = UserRepo(session)
    tests = await test_repo.all()
    for test_obj in tests:
        await msg.answer(test_obj.text)

# States can be set:
# async def set_state(msg: types.Message, state: FSMContext) -> None:
#     await state.set_state(st.SomeState.state1)
