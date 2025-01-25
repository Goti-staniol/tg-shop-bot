from bot.state import UserState
from bot.func import (
    generate_keyboard, 
    disable_keyboard, 
    remove_space, 
    update_keyboard
)

from bot import bot
from bot.kb.inline import (
    product_buy_kb,
    home_btn,
    proof_of_purchase_kb,
    review_kb
)

from data.cfg import html, texts

from db.methods import (
    get_products, 
    get_products_id, 
    get_product,
    get_purchase_status,
    update_product,
    get_file_type,
    add_comment_to_product,
    add_mark,
    deduction_mark,
    get_user_by_product,
    transfer_funds
)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

purchases_router = Router()


@purchases_router.callback_query(F.data == 'back_to_products')
@purchases_router.callback_query(F.data == 'market')
async def user_products_hadler(cb: CallbackQuery) -> None:
    page = 1
    products = get_products()
    products_slice = products[(page - 1) * 7:page * 7]
    total_pages = (len(products) + 7 - 1) // 7
    keyboard = generate_keyboard(
        product_slice=products_slice,
        current_page=page,
        total_pages=total_pages,
        startswith='marketpage_',
        search_btn=True
    )
    
    await cb.message.answer(
        text='Товары:',
        reply_markup=keyboard
    )


@purchases_router.callback_query(F.data.startswith('marketpage_'))
async def pages_handler(cb: CallbackQuery) -> None:
    page = int(cb.data.split('_')[1])
    products = get_products()
    products_slice = products[(page - 1) * 7:page * 7]
    total_pages = (len(products) + 7 - 1) // 7
    keyboard = generate_keyboard(
        product_slice=products_slice,
        current_page=page,
        total_pages=total_pages,
        startswith='marketpage_',
        search_btn=True
    )
    
    await cb.message.edit_text(
        text='Товары:',
        reply_markup=keyboard
    )


@purchases_router.callback_query(
    lambda cb: cb.data in get_products_id(
        cb.from_user.id,
        False,
        False
    )
)
async def open_product_handler(cb: CallbackQuery) -> None:
    product = get_product(cb.data)
    
    if product:
        values = {
            'product_name': product.product_name,
            'product_price': product.product_price,
            'product_description': product.product_description + '\n'\
                if product.product_description else 'Отсутсвует!',
            'product_id': product.product_id
        }
        keyboard = product_buy_kb(product.product_id)

        if not product.product_image:
            await cb.message.answer(
                text=texts['product_txt'].format(**values),
                parse_mode=html,
                reply_markup=keyboard
            )
        else:
            await cb.message.answer_photo(
                photo=product.product_image,
                caption=texts['product_txt'].format(**values),
                parse_mode=html,
                reply_markup=keyboard
            )


@purchases_router.callback_query(F.data.startswith('buy_'))
async def buy_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )

    product = get_product(cb.data.split('_')[1])
    seller_id = get_user_by_product(product.product_id)
    price = product.product_price
    
    await state.update_data(product_id=product.product_id)
    
    if not get_purchase_status(product.product_id):
        status = transfer_funds(
            sender_id=cb.from_user.id,
            recipient_id=seller_id,
            amount_money=price
        )
        
        if status:
            update_product(product.product_id, cb.from_user.id)
            
            desc = remove_space(f'''\
                <b>⚠️Проверяйте данные сразу!⚠️</b>
                        
                {product.text_to_receive if product.text_to_receive else None}
            ''')
            file_to_receive = product.file_to_receive\
                if product.file_to_receive else None
            file_type = get_file_type(product.product_id)
            
            match file_type:
                case 'text':
                    await cb.message.answer(
                        text=desc,
                        parse_mode=html,
                        reply_markup=proof_of_purchase_kb
                    )
                case 'photo':
                    await cb.message.answer_photo(
                        photo=file_to_receive,
                        caption=desc,
                        parse_mode=html,
                        reply_markup=proof_of_purchase_kb
                    )
                case 'video':
                    await cb.message.answer_video(
                        video=file_to_receive,
                        caption=desc,
                        parse_mode=html,
                        reply_markup=proof_of_purchase_kb
                    )
                case 'document':
                    await cb.message.answer_document(
                        document=file_to_receive,
                        caption=desc,
                        parse_mode=html,
                        reply_markup=proof_of_purchase_kb
                    )
        else:
            await cb.answer(
                text='Недостаточно средств на балансе!',
                show_alert=True
            )
    else:
        await cb.message.answer(
            text='<b>Сожелеем! Товар был куплен!</b>',
            parse_mode=html
        )
        

@purchases_router.callback_query(F.data == 'confirm')
async def confirm_handler(cb: CallbackQuery) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    
    await cb.message.answer(
        text='<b>Благодарим за покупку! Отсавьте отзыв, если не сложно!</b>',
        parse_mode=html,
        reply_markup=review_kb
    )


@purchases_router.callback_query(F.data == 'add_comment')
async def add_comment_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    
    await cb.message.answer(
        text='<b>Введите коментарий:</b>',
        parse_mode=html
    )
    
    await state.set_state(UserState.wait_comment)


@purchases_router.message(UserState.wait_comment, F.text)
async def add_comment(msg: Message, state: FSMContext) -> None:
    if msg.text:
        data = await state.get_data()
        
        add_comment_to_product(
            user_id=msg.from_user.id,
            product_id=data.get('product_id'),
            comment=msg.text
        )
        
        await msg.answer(
            text='<b>Коментарий добавлен!</b>',
            parse_mode=html
        )

        await msg.answer(
            text='\
            <b>Благодарим за покупку! Отсавьте отзыв, если не сложно!</b>',
            parse_mode=html,
            reply_markup=review_kb
        )
    else:
        await msg.answer(
            text='<b>Коментарий должен содержать только текст!</b>',
            parse_mode=html
        )


@purchases_router.callback_query(F.data.startswith('mark_'))
async def mark_handler(cb: CallbackQuery, state: FSMContext) -> None:
    mark = cb.data.split('_')[1]
    update_btns = {}

    data = await state.get_data()
    positive_mark = data.get('positive_mark', False)
    negative_mark = data.get('negative_mark', False)
    
    if mark == 'positive':
        if not positive_mark:
            if negative_mark:
                deduction_mark(cb.from_user.id, 'negative')
                await state.update_data(negative_mark=False)
            add_mark(cb.from_user.id, 'positive')
            await state.update_data(positive_mark=True)

    if mark == 'negative':
        if not negative_mark:
            if positive_mark:
                deduction_mark(cb.from_user.id, 'positive')
                await state.update_data(positive_mark=False)
            add_mark(cb.from_user.id, 'negative')
            await state.update_data(negative_mark=True)

    if positive_mark:
        update_btns['mark_positive'] = ('*👍*', 'disable_mark_positive')
    else:
        update_btns['disable_mark_positive'] = ('👍', 'mark_positive')

    if negative_mark:
        update_btns['mark_negative'] = ('*👎*', 'disable_mark_negative')
    else:
        update_btns['disable_mark_negative'] = ('👎', 'mark_negative')

    if positive_mark or negative_mark:
        keyboard = update_keyboard(
            keyboard=review_kb,
            data=update_btns
        )

        try:
            await cb.message.edit_reply_markup(reply_markup=keyboard)
        except TelegramBadRequest:
            pass

@purchases_router.callback_query(F.data == 'ready')
async def ready_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.message.delete()


@purchases_router.callback_query(F.data == 'search_product')
async def search_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    
    sent_msg = await cb.message.answer(
        text='<b>Введи ID товара:</b>',
        parse_mode=html,
        reply_markup=home_btn
    )
    
    await state.update_data(sent_msg_id=sent_msg.message_id)
    await state.set_state(UserState.wait_product_id)


@purchases_router.message(UserState.wait_product_id, F.text)
async def search_product(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    sent_msg_id = data.get('sent_msg_id')

    await bot.delete_message(
        chat_id=msg.chat.id,
        message_id=sent_msg_id
    )
    
    product = get_product(msg.text)
    if product:
        values = {
            'product_name': product.product_name,
            'product_price': product.product_price,
            'product_description': product.product_description + '\n'\
                if product.product_description else 'Отсутсвует!',
            'product_id': product.product_id
        }
        keyboard = product_buy_kb(product.product_id)

        if not product.product_image:
            await msg.answer(
                text=texts['product_txt'].format(**values),
                parse_mode=html,
                reply_markup=keyboard
            )
        else:
            await msg.answer_photo(
                photo=product.product_image,
                caption=texts['product_txt'].format(**values),
                parse_mode=html,
                reply_markup=keyboard
            )
    else:
        await msg.answer(
            text='<b>Данный товар не был найден на рынке!</b>',
            parse_mode=html,
            reply_markup=home_btn
        )

    await state.clear()