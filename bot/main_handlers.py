from data.cfg import texts, html

from .kb.inline import menu_inl_kb, agree_btn
from .kb.markup import menu_keyboard

from db.methods import add_user, get_agreement, update_user_agreement

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

main_router = Router()


@main_router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext) -> None:
    if not get_agreement(msg.chat.id):
        global sent_msg
        sent_msg = await msg.answer(
            text=texts['agreement_text'],
            parse_mode=html,
            reply_markup=agree_btn
        )
        msg.edit_reply_markup()
    else:
        await msg.answer(
            text=texts['welcome_txt'],
            parse_mode=html,
            reply_markup=menu_inl_kb)
    await state.clear()

@main_router.callback_query(F.data == 'agree')
async def handler_agree(cb: CallbackQuery) -> None:
    await sent_msg.delete()
    add_user(cb.from_user.id)
    update_user_agreement(cb.from_user.id)

