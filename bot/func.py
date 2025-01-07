from textwrap import dedent
from typing import Dict, Tuple
from bot.kb import InlineKeyboardMarkup, InlineKeyboardButton

def remove_space(text: str) -> str:
    return dedent(text)

def update_keyboard(
    keyboard: list, 
    data: Dict[str, Tuple[str, str]],
) -> list:
    for buttons in keyboard.inline_keyboard:
        for button in buttons:
            if button.callback_data in data:
                new_text, new_callback = data[button.callback_data]
                button.text = new_text
                button.callback_data = new_callback

    return keyboard

def disable_keyboard(keyboard: list) -> list:
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
            Цена: <b>{price_product}</b>
            ==================================
            Описание: <b>{description_product}</b>
        ''')