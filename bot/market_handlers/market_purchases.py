from bot.func import generate_keyboard
from data.cfg import html, texts

from db.methods import (
    get_products, 
    get_products_id, 
    get_product, 
    is_user_owner_of_product
)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

purchases_router = Router()


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


@purchases_router.callback_query(lambda cb: cb.data in get_products_id())
async def open_product_handler(cb: CallbackQuery) -> None:
    product = get_product(cb.data)
    if product:
            values = {
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_description': product.product_description\
                    if product.product_description else 'Отсутсвует!',
                'product_id': product.product_id
            }
        # if not is_user_owner_of_product(cb.from_user.id, product.product_id):
            if not product.product_image:
                await cb.message.answer(
                    text=texts['product_txt'].format(**values),
                    parse_mode=html
                )
            else:
                await cb.message.answer_photo(
                    photo=product.product_image,
                    caption=texts['product_txt'].format(**values),
                    parse_mode=html
                )
        # else:
        #     print('Вы владелец')


@purchases_router.callback_query(F.data == 'search_product')
async def search_handler(cb: CallbackQuery) -> None:
    ...