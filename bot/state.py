from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    wait_name = State()
    wait_description = State()
    wait_price = State()
    wait_image = State()
    wait_product = State()
    wait_product_id = State()
    wait_comment = State()
    wait_amount = State()
    wait_amount_to_withdraw = State()