from data.cfg import texts, html
from .func import disable_keyboard, generate_keyboard, update_keyboard

from .state import UserState

from .kb.markup import menu_keyboard
from .kb.inline import (
    menu_inl_kb, 
    agree_btn, 
    profile_kb,
    my_purchases_kb
)

from db.methods import (
    add_user, 
    get_agreement, 
    update_user_agreement,
    get_products_user,
    get_user_purchases,
    balance_refill,
    get_user_amount,
    get_user_rating,
    get_product,
    get_file_type,
    withdraw_money,
    transfer_to_avaible
)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

main_router = Router()


@main_router.message(F.text == '🏠 Домой')
@main_router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext) -> None:
    if not get_agreement(msg.chat.id):
        sent_msg = await msg.answer(
            text=texts['agreement_txt'],
            parse_mode=html,
            reply_markup=agree_btn
        )
        await state.update_data(sent_msg=sent_msg)
    else:
        await msg.answer(
            text=texts['welcome_txt'],
            parse_mode=html,
            reply_markup=menu_inl_kb
        )
        await msg.answer(
            text='Не забывайте следить за нашими новостями!',
            reply_markup=menu_keyboard
        )
        await state.clear()



@main_router.callback_query(F.data == 'agree')
async def agree_handler(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    sent_msg = data.get('sent_msg')

    if sent_msg:
        await sent_msg.delete()

    add_user(cb.from_user.id)
    update_user_agreement(cb.from_user.id)

    await start_handler(cb.message, state)


@main_router.callback_query(F.data == 'home')
async def home_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await start_handler(cb.message, state)
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )


@main_router.message(F.text == '👤 Профиль')
async def profile_handler(msg: Message) -> None:
    deal_count, percent = get_user_rating(msg.from_user.id)
    values = {
        'user_id': msg.from_user.id,
        'user_amount': get_user_amount(msg.from_user.id),
        'deal_count': deal_count,
        'user_rating': percent
    }
    await msg.answer(
        text=texts['profile_txt'].format(**values),
        parse_mode=html,
        reply_markup=profile_kb
    )


@main_router.callback_query(F.data == 'add_funds')
async def add_funds_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.answer(
        text='<b>Введи сумму на которую хочешь пополнить:</b>',
        parse_mode=html,
    )
    
    await state.set_state(UserState.wait_amount)


@main_router.message(UserState.wait_amount, F.text)
async def add_funds(msg: Message, state: FSMContext) -> None:
    try:
        amount = round(float(msg.text), 2)
        balance_refill(msg.from_user.id, amount)
        await msg.answer(
            text=f'<b>Баланс успешно пополнен на</b> <code>{amount}</code>',
            parse_mode=html
        )
        await state.clear()
    except ValueError:
        await msg.answer(
            text='<b>Некоректная сумма! Пример:</b> <code>1.0, 1</code>',
            parse_mode=html
        )
        await state.set_state(UserState.wait_amount)


@main_router.callback_query(F.data == 'withdraw_funds')
async def withdraw_funds_handler(cb: CallbackQuery, state: FSMContext) -> None:
    transfer_to_avaible(cb.from_user.id)

    await cb.message.answer(
        text='<b>Укажите смму на вывод:</b>',
        parse_mode=html
    )

    await state.set_state(UserState.wait_amount_to_withdraw)


@main_router.callback_query(UserState.wait_amount_to_withdraw, F.text)
async def withdraw_money(msg: Message, state: FSMContext) -> None:
    ... #TODO Сделать вывод


@main_router.callback_query(F.data == 'my_products')
async def user_products_handler(cb: CallbackQuery) -> None:
    products = get_products_user(cb.from_user.id)
    
    if len(products) != 0:
        page = 1
        products_slice = products[(page - 1) * 5:page * 5]
        total_pages = (len(products) + 5 - 1) // 5
        keyboard = generate_keyboard(
            product_slice=products_slice,
            current_page=page,
            total_pages=total_pages,
            startswith='mypage_'
        )
        await cb.message.answer(
            text='Ваши товары:',
            reply_markup=keyboard
        )
    else:
        await cb.message.answer(
            text='У вас пока нет товаров!'
        )


@main_router.callback_query(F.data.startswith('mypage_'))
async def pages_handler(cb: CallbackQuery) -> None:
    page = int(cb.data.split('_')[1])
    products = get_products_user(cb.from_user.id)
    products_slice = products[(page - 1) * 5:page * 5]
    total_pages = (len(products) + 5 - 1) // 5
    keyboard = generate_keyboard(
        product_slice=products_slice,
        current_page=page,
        total_pages=total_pages,
        startswith='mypage_'
    )
    await cb.message.edit_text(
        text='Ваши товары:',
        reply_markup=keyboard
    )


@main_router.callback_query(F.data == 'back_to_purchases')
@main_router.callback_query(F.data == 'my_purchases')
async def my_purchases_handler(cb: CallbackQuery) -> None:
    user_purchases = get_user_purchases(cb.from_user.id)
    
    if len(user_purchases) != 0:
        page = 1
        products_slice = user_purchases[(page - 1) * 5:page * 5]
        total_pages = (len(user_purchases) + 5 - 1) // 5
        keyboard = generate_keyboard(
            product_slice=products_slice,
            current_page=page,
            total_pages=total_pages,
            startswith='mypurchasespage_'
        )

        await cb.message.answer(
            text='<b>Список ваших покупок:</b>',
            parse_mode=html,
            reply_markup=keyboard
        )
    else:
        await cb.answer(
            text='У вас нет покупок!'
        )


@main_router.callback_query(F.data.startswith('mypurchasespage_'))
async def purchases_page_handler(cb: CallbackQuery) -> None:
    page = int(cb.data.split('_')[1])
    user_purchases = get_user_purchases(cb.from_user.id)
    products_slice = user_purchases[(page - 1) * 5:page * 5]
    total_pages = (len(user_purchases) + 5 - 1) // 5
    keyboard = generate_keyboard(
        product_slice=products_slice,
        current_page=page,
        total_pages=total_pages,
        startswith='mypurchasespage_'
    )
    
    await cb.message.edit_text(
        text='<b>Список ваших покупок:</b>',
        parse_mode=html,
        reply_markup=keyboard
    )


@main_router.callback_query(
    lambda cb: cb.data in [
        product.product_id for product in get_user_purchases(cb.from_user.id)
    ]
)
async def user_purchases_handler(cb: CallbackQuery, state: FSMContext) -> None:
    product = get_product(cb.data)

    if product:
        values = {
            'product_name': product.product_name,
            'product_price': product.product_price,
            'product_buy_time': 12,
            'product_desc': product.product_description\
                if product.product_description else 'Отсутсвует',
            'product_id': product.product_id
        }
        
        await cb.message.answer(
            text=texts['buy_product_txt'].format(**values),
            parse_mode=html,
            reply_markup=my_purchases_kb
        )

        await state.update_data(product_to_view=product.product_id)


@main_router.callback_query(F.data == 'view_content')
async def view_content_handler(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    product_id = data.get('product_to_view')
    product = get_product(product_id)

    if product:
        file_type = get_file_type(product.product_id)
        desc = product.text_to_receive
        file_to_receive = product.file_to_receive

        match file_type:
            case 'text':
                await cb.message.answer(
                    text=desc,
                    parse_mode=html,
                )
            case 'photo':
                await cb.message.answer_photo(
                    photo=file_to_receive,
                    caption=desc,
                    parse_mode=html,
                )
            case 'video':
                await cb.message.answer_video(
                    video=file_to_receive,
                    caption=desc,
                    parse_mode=html,
                )
            case 'document':
                await cb.message.answer_document(
                    document=file_to_receive,
                    caption=desc,
                    parse_mode=html,
                )


