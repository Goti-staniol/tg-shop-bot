from . import KeyboardButton, ReplyKeyboardMarkup

menu_btn = [
    [KeyboardButton(text='👤 Профиль')]
]

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=menu_btn,
    resize_keyboard=True,
    selective=True
)