from . import KeyboardButton, ReplyKeyboardMarkup

menu_btn = [
    [KeyboardButton(text='Маркет')],
    [KeyboardButton(text='Профиль'), KeyboardButton(text='Пополнение')]
]

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=menu_btn,
    resize_keyboard=True
)