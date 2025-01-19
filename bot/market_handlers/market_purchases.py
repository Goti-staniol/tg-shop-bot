from bot.state import UserState
from bot.func import (
    generate_keyboard, 
    disable_keyboard, 
    remove_space, 
    update_keyboard
)

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
    is_user_owner_of_product,
    get_purchase_status,
    update_product,
    get_file_type,
    is_buyer_of_product,
    add_comment_to_product,
    add_mark,
    deduction_mark,
    get_user_by_product,
    transfer_funds
)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

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
        text='товары:',
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
        text='товары:',
        reply_markup=keyboard
    )


@purchases_router.callback_query(lambda cb: cb.data in get_products_id(False))
async def open_product_handler(cb: CallbackQuery) -> None:
    product = get_product(cb.data)
    
    if product:
        # if not is_user_owner_of_product(cb.from_user.id, product.product_id):
            # if not is_buyer_of_product(cb.from_user.id, product.product_id):
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
            # else:
            #     await cb.message.answer(
            #         'Вы купили этот продукт'
            #     )
        # else:
        #     print('Вы владелец')


@purchases_router.callback_query(F.data.startswith('buy_'))
async def buy_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    product = get_product(cb.data.split('_')[1])
    saller_id = get_user_by_product(product.product_id)
    price = product.product_price
    
    await state.update_data(product_id=product.product_id)
    
    if not get_purchase_status(product.product_id):
        status = transfer_funds(
            sender_id=cb.from_user.id,
            recipient_id=saller_id,
            amount_money=price
        )
        
        if status:
            update_product(product.product_id, cb.from_user.id)
            
            desc = remove_space(f'''\
                <b>⚠️Проверяйте данные сразу!⚠️</b>
                        
                {product.text_to_receive}
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
async def confirm_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    
    review_msg = await cb.message.answer(
        text='<b>Благодарим за покупку! Отсавьте отзыв, если не сложно!</b>',
        parse_mode=html,
        reply_markup=review_kb
    )
    
    await state.update_data(review_msg=review_msg)


@purchases_router.callback_query(F.data == 'add_comment')
async def add_comment_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    
    await cb.message.answer(
        '<b>Введите коментарий:</b>',
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
    else:
        await msg.answer(
            text='<b>Коментарий должен содержать только текст!</b>',
            parse_mode=html
        )


@purchases_router.callback_query(F.data.startswith('mark_'))
async def mark_handler(cb: CallbackQuery, state: FSMContext) -> None:
    mark = cb.data.split('_')[1]
    update_btn = {}

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
    
    await state.update_data(sent_msg=sent_msg)
    await state.set_state(UserState.wait_product_id)


@purchases_router.message(UserState.wait_product_id, F.text)
async def search_product(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    sent_msg = data.get('sent_msg')
    state.clear()
    
    await sent_msg.delete()
    
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
        msg.answer(
            text='<b>Данный товар не был найден на рынке!</b>',
            parse_mode=html,
            reply_markup=home_btn
        )