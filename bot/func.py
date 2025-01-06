from textwrap import dedent

def remove_space(text: str) -> str:
    return dedent(text)

def update_keyboard(
    keyboard: list, 
    callback_data: str,
    new_text: str | int,
    new_callback_data: str
    ) -> list:
    for buttons in keyboard.inline_keyboard:
        for button in buttons:
            if button.callback_data == callback_data:
                button.text = new_text
                button.callback_data = new_callback_data
    return keyboard