from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlite_aio.sqlite import get_check_lst, is_admin, get_checks, add_checks, del_checks, add_admins, del_admins, get_admins
from core.utils.statescheck_admin import AdminStates, CheckStates

async def get_check_edit_form(message:Message, state:FSMContext):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl_1 = await get_check_lst(user_id, username)
    fl = await is_admin(user_id, username)
    if fl and fl_1:
        lst = await get_checks()
        txt = f'\n'.join(lst)
        await message.answer(f'Список телеграм-id, у которых есть доступ к боту:')
        await message.answer(txt)
        await message.answer(f'Выберите дальнейшее действие: Удалить/Добавить или Отмена (выбранное отправьте в ответ)')
        await state.set_state(CheckStates.GET_DEL_OR_ADD)
    else:
        await message.answer(f"Этот раздел не для Вас")

async def get_check_id(message:Message, state:FSMContext):
    ans = message.text
    if ans == "Удалить":
        await state.update_data(ans = ans)
        await message.answer(f"Введите телеграмм-id для удаления (без значка @)")
        await state.set_state(CheckStates.GET_CHECKS_ID)
    elif ans == "Добавить":
        await state.update_data(ans = ans)
        await message.answer(f"Введите телеграмм-id для добавления (без значка @)")
        await state.set_state(CheckStates.GET_CHECKS_ID)
    elif ans == "Отмена":
        await message.answer(f"Редактирование отменено.")
        await state.clear()
    else:
        await message.answer(f"Такого варианта ответа не было. Повторите попытку.")
        await state.clear()

async def checks_edit(message:Message, state:FSMContext):
    data = await state.get_data()
    ans = data.get("ans")
    tg_id = message.text
    if ans == "Удалить":
        fl = await del_checks(tg_id)
        if fl:
            await message.answer(f"Телеграмм-id успешно удален")
        else:
            await message.answer(f"Произошла ошибка, повторите позже")
        await state.clear()
    else:
        fl = await add_checks(tg_id)
        if fl:
            await message.answer(f"Телеграмм-id успешно добавлен")
        else:
            await message.answer(f"Произошла ошибка, повторите позже")
        await state.clear()

async def get_admin_edit_form(message:Message, state:FSMContext):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl_1 = await get_check_lst(user_id, username)
    fl = await is_admin(user_id, username)
    if fl and fl_1:
        lst = await get_admins()
        txt = f'\n'.join(lst)
        await message.answer(f'Список телеграм-id администраторов:')
        await message.answer(txt)
        await message.answer(f'Выберите дальнейшее действие: Удалить/Добавить или Отмена (выбранное отправьте в ответ)')
        await state.set_state(AdminStates.GET_DEL_OR_ADD)
    else:
        await message.answer(f"Этот раздел не для Вас")

async def get_admin_id(message:Message, state:FSMContext):
    ans = message.text
    if ans == "Удалить":
        await state.update_data(ans = ans)
        await message.answer(f"Введите телеграмм-id для удаления (без значка @)")
        await state.set_state(AdminStates.GET_ADMINS_ID)
    elif ans == "Добавить":
        await state.update_data(ans = ans)
        await message.answer(f"Введите телеграмм-id для добавления (без значка @)")
        await state.set_state(AdminStates.GET_ADMINS_ID)
    elif ans == "Отмена":
        await message.answer(f"Редактирование отменено.")
        await state.clear()
    else:
        await message.answer(f"Такого варианта ответа не было. Повторите попытку.")
        await state.clear()

async def admins_edit(message:Message, state:FSMContext):
    data = await state.get_data()
    ans = data.get("ans")
    tg_id = message.text
    if ans == "Удалить":
        fl = await del_admins(tg_id)
        if fl:
            await message.answer(f"Телеграмм-id успешно удален")
        else:
            await message.answer(f"Произошла ошибка, повторите позже")
        await state.clear()
    else:
        fl = await add_admins(tg_id)
        if fl:
            await message.answer(f"Телеграмм-id успешно добавлен")
        else:
            await message.answer(f"Произошла ошибка, повторите позже")
        await state.clear()
