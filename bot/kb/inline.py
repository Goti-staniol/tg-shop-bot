from . import InlineKeyboardButton, InlineKeyboardMarkup

menu_inl_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='🛍️ Катлог', 
        callback_data='market'
    )],
    [InlineKeyboardButton(
        text='📦 Выставить товар', 
        callback_data='add_product'
    )],
    [InlineKeyboardButton(
        text="💬 Чат с поддержкой", 
        callback_data="contact_support"
    )]
]) 

agree_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Я согласен!', callback_data='agree')]
])

add_product_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='Добавить название',
        callback_data='add_name'
    ), InlineKeyboardButton(
        text='Добавить описание',
        callback_data='add_desc'
    )],
    [InlineKeyboardButton(
        text='Добавить фото',
        callback_data='add_image'
    ), InlineKeyboardButton(
        text='Добавить цену',
        callback_data='add_price'
    )],
    [InlineKeyboardButton(
        text='Дальше',
        callback_data='further'
    )]
])

# [InlineKeyboardButton(text='📜 Пользовательское соглашение', callback_data='agreement')]