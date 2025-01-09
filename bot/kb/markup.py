from . import KeyboardButton, ReplyKeyboardMarkup

menu_btn = [
    [
        KeyboardButton(text='👤 Профиль'),
        KeyboardButton(text='🏠 Домой')
    ],
    [
        KeyboardButton(text='🔍 Найти товар')
    ]
]

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=menu_btn,
    resize_keyboard=True,
    selective=True
)