from textwrap import dedent
from typing import Dict, Tuple

from aiogram.types import ReplyKeyboardMarkup

from bot.kb import InlineKeyboardMarkup, InlineKeyboardButton

def remove_space(text: str) -> str:
    return dedent(text)

def update_keyboard(
    keyboard: InlineKeyboardMarkup,
    data: Dict[str, Tuple[str, str]],
) -> InlineKeyboardMarkup:
    for buttons in keyboard.inline_keyboard:
        for button in buttons:
            if button.callback_data in data:
                new_text, new_callback = data[button.callback_data]
                button.text = new_text
                button.callback_data = new_callback

    return keyboard

def disable_keyboard(keyboard: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    for buttons in keyboard.inline_keyboard:
        for button in buttons:
            button.callback_data = 'disable'

    return keyboard
    
def update_product_text(
    name_product: str = None,
    description_product: str = None,
    price_product: str = None
) -> str:
    name_product = name_product if name_product is not None\
        else 'Обьязательно'
    price_product = price_product if price_product is not None\
        else 'Обьязательно'
    
    if description_product:
        description_product = description_product
    else:
        description_product = 'Не обьязательно'
            
    return remove_space(f'''
            Название: <b>{name_product}</b>
            Цена: <b>{price_product} $</b>
            ==================================
            Описание: <b>{description_product}</b>
        ''')

def generate_keyboard(
    product_slice: list,
    current_page: int,
    total_pages: int,
    startswith: str,
    search_btn: bool = False
) -> InlineKeyboardMarkup:
    btn_list = []
    navigation_btns = []
    
    if search_btn:
        btn_list.append(
            [InlineKeyboardButton(
                text='🔍 Найти товар',
                callback_data='search_product'
            )]
        )
    
    for product in product_slice:
        btn_list.append(
            [InlineKeyboardButton(
                text=product.product_name,
                callback_data=product.product_id
            )]
        )
        
    if current_page > 1:
        navigation_btns.append(
            InlineKeyboardButton(
                text="⬅️ Назад", 
                callback_data=f"{startswith}{current_page - 1}"
            )
        )
    if current_page < total_pages:
        navigation_btns.append(
            InlineKeyboardButton(
                text="Вперед ➡️", 
                callback_data=f"{startswith}{current_page + 1}"
            )
        )
    if navigation_btns:
        btn_list.append(navigation_btns)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=btn_list)
    
    return keyboard