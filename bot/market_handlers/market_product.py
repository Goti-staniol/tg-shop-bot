from bot.kb.inline import add_product_kb, back_btn, home_btn
from bot.state import UserState
from bot.func import (
    disable_keyboard,
    remove_space,
    update_product_text,
    update_keyboard
)

from data.cfg import html, texts
from db.methods import add_new_product

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import uuid

product_router = Router()


@product_router.callback_query(F.data == 'add_product')
async def add_item_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )

    await cb.message.answer(
        text=update_product_text(),
        parse_mode=html,
        reply_markup=add_product_kb
    )


@product_router.callback_query(F.data == 'add_name')
async def add_name_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    await cb.message.answer(
        text='Введи название товара! Не больше 50 символов!',
        reply_markup=back_btn
    )
    await state.set_state(UserState.wait_name)


@product_router.message(UserState.wait_name, F.text)
async def add_name_product(msg: Message, state: FSMContext) -> None:
    if len(msg.text) < 50:
        await state.update_data(name=msg.text)
        await msg.answer('Имя успешно добавлено!')

        data = await state.get_data()

        update_btns = {
            'add_name': (
                'Удалить название', 'del_name'
            ) if data.get('name') else (
                'Добавить название', 'add_name'
            ),
            'add_desc': (
                'Удалить описание', 'del_desc'
            ) if data.get('desc') else (
                'Добавить описание', 'add_desc'
            ),
            'add_price': (
                'Удалить цену', 'del_price'
            ) if data.get('price') else (
                'Добавить цену', 'add_price'
            ),
            'add_image': (
                'Удалить фотографию', 'del_image'
            ) if data.get('image_id') else (
                'Добавить фотографию', 'add_image'
            ),
        }

        keyboard = update_keyboard(add_product_kb, update_btns)
        await msg.answer(
            text=update_product_text(
                name_product=data.get('name'),
                description_product=data.get('desc'),
                price_product=data.get('price')
            ),
            parse_mode=html,
            reply_markup=keyboard
        )
    else:
        await msg.answer(
            text='Cлишком длинное имя! Попробуйте еще раз!',
            reply_markup=back_btn
        )


@product_router.callback_query(F.data == 'add_desc')
async def add_desc_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    await cb.message.answer(
        text='Введи описание товара! Не больше 200 символов!',
        reply_markup=back_btn
    )
    await state.set_state(UserState.wait_description)


@product_router.message(UserState.wait_description, F.text)
async def add_description(msg: Message, state: FSMContext) -> None:
    if len(msg.text) < 200:
        await state.update_data(desc=msg.text)
        await msg.answer('Описание успешно добавлено!')

        data = await state.get_data()

        update_btns = {
            'add_name': (
                'Удалить название', 'del_name'
            ) if data.get('name') else (
                'Добавить название', 'add_name'
            ),
            'add_desc': (
                'Удалить описание', 'del_desc'
            ) if data.get('desc') else (
                'Добавить описание', 'add_desc'
            ),
            'add_price': (
                'Удалить цену', 'del_price'
            ) if data.get('price') else (
                'Добавить цену', 'add_price'
            ),
            'add_image': (
                'Удалить фотографию', 'del_image'
            ) if data.get('image_id') else (
                'Добавить фотографию', 'add_image'
            ),
        }

        keyboard = update_keyboard(add_product_kb, update_btns)
        await msg.answer(
            text=update_product_text(
                name_product=data.get('name'),
                description_product=data.get('desc'),
                price_product=data.get('price')
            ),
            parse_mode=html,
            reply_markup=keyboard
        )
    else:
        await msg.answer(remove_space(
            '''
            Слишком длинное описание!
            Если вы хотите передать инстуркцию, передайте ее текстовым  файлом!
            '''
        ))


@product_router.callback_query(F.data == 'add_image')
async def add_image_handler(cb:  CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    await cb.message.answer(
        text='Отправьте фотографию:',
        reply_markup=back_btn
    )
    await state.set_state(UserState.wait_image)


@product_router.message(UserState.wait_image, F.photo)
async def add_image(msg: Message, state: FSMContext) -> None:
    image = msg.photo[-1].file_id
    data = await state.get_data()

    await state.update_data(image_id=image)
    await msg.answer(f'Фотография успешно добавлена!')

    update_btns = {
        'add_name': (
            'Удалить название', 'del_name'
        ) if data.get('name') else (
            'Добавить название', 'add_name'
        ),
        'add_desc': (
            'Удалить описание', 'del_desc'
        ) if data.get('desc') else (
            'Добавить описание', 'add_desc'
        ),
        'add_price': (
            'Удалить цену', 'del_price'
        ) if data.get('price') else (
            'Добавить цену', 'add_price'
        ),
        'add_image': (
            'Удалить фотографию', 'del_image'
        ) if data.get('image_id') else (
            'Добавить фотографию', 'add_image'
        ),
    }

    keyboard = update_keyboard(add_product_kb, update_btns)
    await msg.answer(
        text=update_product_text(
            name_product=data.get('name'),
            description_product=data.get('desc'),
            price_product=data.get('price')
        ),
        parse_mode=html,
        reply_markup=keyboard
    )


@product_router.callback_query(F.data == 'add_price')
async def add_price_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )
    await cb.message.answer(
        text='Введи цену за товар:',
        reply_markup=back_btn
    )
    await state.set_state(UserState.wait_price)


@product_router.message(UserState.wait_price, F.text)
async def add_price(msg: Message, state: FSMContext) -> None:
    try:
        price = round(float(msg.text), 2)
        await state.update_data(price=price)

        data = await state.get_data()

        update_btns = {
            'add_name': (
                'Удалить название', 'del_name'
            ) if data.get('name') else (
                'Добавить название', 'add_name'
            ),
            'add_desc': (
                'Удалить описание', 'del_desc'
            ) if data.get('desc') else (
                'Добавить описание', 'add_desc'
            ),
            'add_price': (
                'Удалить цену', 'del_price'
            ) if data.get('price') else (
                'Добавить цену', 'add_price'
            ),
            'add_image': (
                'Удалить фотографию', 'del_image'
            ) if data.get('image_id') else (
                'Добавить фотографию', 'add_image'
            ),
        }

        keyboard = update_keyboard(add_product_kb, update_btns)
        await msg.answer(
            text=update_product_text(
                name_product=data.get('name'),
                description_product=data.get('desc'),
                price_product=data.get('price')
            ),
            parse_mode=html,
            reply_markup=keyboard
        )
    except ValueError:
        await msg.answer(
            text='Цена должна быть числом! Пример: 1, 1.0',
            reply_markup=back_btn
        )


@product_router.callback_query(F.data == 'further')
async def validate_data(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    name = data.get('name')
    price = data.get('price')

    if name and price:
        await cb.message.answer(
            texts['warning_txt'],
            parse_mode=html,
            reply_markup=back_btn
        )
        await state.set_state(UserState.wait_product)
    else:
        await cb.answer('Имя и цена обьязательны!', show_alert=True)


@product_router.message(UserState.wait_product)
async def public_router(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    name = data.get('name')
    description = data.get('desc')
    price = data.get('price')
    image_id = data.get('image_id')
    product_id = str(uuid.uuid4())

    if msg.text:
        content = ('', msg.text)
        file_type = 'text'
    elif msg.photo:
        receive_image_id = msg.photo[-1].file_id
        caption = msg.caption if msg.caption else ''
        content = (receive_image_id, caption)
        file_type = 'photo'
    elif msg.video:
        video_id = msg.video.file_id
        caption = msg.caption if msg.caption else ''
        content = (video_id, caption)
        file_type = 'video'
    elif msg.document:
        file_id = msg.document.file_id
        caption = msg.caption if msg.caption else ''
        content = (file_id, caption)
        file_type = 'document'

    add_new_product(
        user_id=msg.from_user.id,
        product_id=product_id,
        product_name=name,
        product_description=description if description else '',
        product_image=image_id if image_id else '',
        product_price=price,
        product_to_receive=content,
        file_type=file_type
    )

    await msg.answer(
        text=texts['info_product_txt'].format(**{'product_id': product_id}),
        parse_mode=html,
        reply_markup=home_btn
    )
    await state.clear()


@product_router.callback_query(F.data == 'back')
async def back_state(cb: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state:
        await state.set_state(None)

    data = await state.get_data()

    update_btns = {
        'add_name': (
            'Удалить название', 'del_name'
        ) if data.get('name') else (
            'Добавить название', 'add_name'
        ),
        'add_desc': (
            'Удалить описание', 'del_desc'
        ) if data.get('desc') else (
            'Добавить описание', 'add_desc'
        ),
        'add_price': (
            'Удалить цену', 'del_price'
        ) if data.get('price') else (
            'Добавить цену', 'add_price'
        ),
        'add_image': (
            'Удалить фотографию', 'del_image'
        ) if data.get('image_id') else (
            'Добавить фотографию', 'add_image'
        ),
    }

    keyboard = update_keyboard(add_product_kb, update_btns)
    await cb.message.answer(
        text=update_product_text(
            name_product=data.get('name'),
            description_product=data.get('desc'),
            price_product=data.get('price')
        ),
        parse_mode=html,
        reply_markup=keyboard
    )

    await cb.message.edit_reply_markup(
        reply_markup=disable_keyboard(cb.message.reply_markup)
    )


@product_router.callback_query(F.data.startswith('del_'))
async def del_name_handler(cb: CallbackQuery, state: FSMContext) -> None:
    update_btns = {}

    if cb.data == 'del_name':
        update_btns['del_name'] = ('Добавить название', 'add_name')
        await state.update_data(name=None)
    elif cb.data == 'del_desc':
        update_btns['del_desc'] = ('Добавить описание', 'add_desc')
        await state.update_data(desc=None)
    elif cb.data == 'del_price':
        update_btns['del_price'] = ('Добавить цену', 'add_price')
        await state.update_data(price=None)
    elif cb.data == 'del_image':
        update_btns['del_image'] = ('Добавить фотографию', 'add_image')
        await state.update_data(image_id=None)

    data = await state.get_data()

    keyboard = update_keyboard(add_product_kb, update_btns)
    await cb.message.edit_text(
        text=update_product_text(
            name_product=data.get('name'),
            description_product=data.get('desc'),
            price_product=data.get('price')
        ),
        parse_mode=html,
        reply_markup=keyboard
    )