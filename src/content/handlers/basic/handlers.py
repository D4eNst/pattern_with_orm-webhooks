import logging

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from repository.crud.users import UserRepo

router = Router()

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    current_state = await state.get_state()
    await message.answer(f"Hi, Im started! Current state is {current_state}")

    user_repo = UserRepo(session)
    try:
        user = await user_repo.get(telegram_id=message.from_user.id)
    except NoResultFound:
        user = await user_repo.create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    await message.answer(f"Hello, {user.username}!")

    all_users = await user_repo.all()
    ans_users = [u.first_name for u in all_users]
    await message.answer(f"All users in bot:\n{', '.join(ans_users)}")
    logger.warning(f"Test log message. List users: {ans_users}")

# States can be set:
# async def set_state(message: types.Message, state: FSMContext) -> None:
#     await state.set_state(st.SomeState.state1)
