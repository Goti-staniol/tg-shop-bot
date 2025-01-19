from . import InlineKeyboardButton, InlineKeyboardMarkup

back_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back')]
])

home_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

menu_inl_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🛍️ Катлог', 
            callback_data='market'
        )
    ],
    [
        InlineKeyboardButton(
            text='📦 Выставить товар', 
            callback_data='add_product'
        )
    ],
    [
        InlineKeyboardButton(
            text="💬 Чат с поддержкой", 
            callback_data="contact_support"
        )
    ]
]) 

agree_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Я согласен!', callback_data='agree')]
])

add_product_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Добавить название',
            callback_data='add_name'
        ), 
        InlineKeyboardButton(
            text='Добавить описание',
            callback_data='add_desc'
        )
    ],
    [
        InlineKeyboardButton(
            text='Добавить фото',
            callback_data='add_image'
        ),  
        InlineKeyboardButton(
            text='Добавить цену',
            callback_data='add_price'
        )
    ],
    [
        InlineKeyboardButton(
            text='Дальше',
            callback_data='further'
        )
    ]
])

profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='📥 Пополнить баланс',
            callback_data='add_funds'
        ), 
        InlineKeyboardButton(
            text='📤 Вывести средства',
            callback_data='withdraw_funds'
        )
    ],
    [
        InlineKeyboardButton(
            text='🛍 Мои товары',
            callback_data='my_products'
        ),
        InlineKeyboardButton(
            text='🛒 Мои покупки',
            callback_data='my_purchases'
        )
    ],
    home_btn.inline_keyboard[0]
])

proof_of_purchase_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='✅ Подтвердить покупку',
            callback_data='confirm'
        )
    ],
    [
        InlineKeyboardButton(
            text='⛔️ Подать жалобу',
            callback_data='report'
        )
    ]
])

review_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='💬 Оставить коментарий',
            callback_data='add_comment'
            
        )
    ],
    [
        InlineKeyboardButton(
            text='👍',
            callback_data='mark_positive'
        ),
        InlineKeyboardButton(
            text='👎',
            callback_data='mark_negative'
        )
    ],
    [
        InlineKeyboardButton(
            text='✅ Готово',
            callback_data='ready'
        )
    ]
])

def product_buy_kb(product_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='🛒 Купить товар',
                callback_data=f'buy_{product_id}'
            )
        ],
        [
            InlineKeyboardButton(
                text='📜 К списку товаров',
                callback_data='back_to_products'
            )
        ]
    ])
# [InlineKeyboardButton(text='📜 Пользовательское соглашение', callback_data='agreement')]
