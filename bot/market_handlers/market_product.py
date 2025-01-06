from bot.kb.inline import add_product_kb

from data.cfg import html
from bot.func import update_keyboard

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


product_router = Router()


class UserState(StatesGroup):
    wait_name = State()


@product_router.callback_query(F.data == 'add_product')
async def add_item_handler(cb: CallbackQuery) -> None:
    await cb.message.answer(
        text='Название: <b>Обьязательно</b>',
        parse_mode=html,
        reply_markup=add_product_kb
    )


@product_router.callback_query(F.data == 'add_name')
async def add_name_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.answer(
        text='Введи название товара! Не больше 50 символов!'
    )
    await state.set_state(UserState.wait_name)


@product_router.message(UserState.wait_name, F.text)
async def add_name_product(msg: Message, state: FSMContext) -> None:
    if len(msg.text) < 50:
        await state.update_data(name=msg.text)
        await msg.answer('Успешно добавлено!')
        
        keyboard = update_keyboard(
            keyboard=add_product_kb,
            callback_data='add_name',
            new_text='Убрать Имя',
            new_callback_data='del_name'
        )
        
        await msg.answer(
            text=f'Название: {msg.text}',
            parse_mode=html,
            reply_markup=keyboard
        )
        
    else:
        await msg.answer('Cлишком длинное имя!')
        await state.set_state(UserState.wait_name)
        
        return
    
